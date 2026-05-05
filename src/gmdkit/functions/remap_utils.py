# Imports
import copy
from typing import Callable, Optional, Sequence
import re

# Package Imports
from gmdkit.casting.id_rules import ID_RULES
from gmdkit.other.id_classes import IDType, IDRule, RuleHandler
from gmdkit import Level, Object, ObjectList
from gmdkit.models.prop.color import ColorList
from gmdkit.mappings import obj_prop, obj_id
from gmdkit.utils.misc import next_free
from gmdkit.functions.object import clean_duplicate_groups
from gmdkit.functions.object_list import compile_keyframe_groups, clean_gid_parents, add_groups


def create_text_id_rule(
        regex:str,
        id_type:IDType,
        condition:Optional[Callable]=None,
        id_min:Optional[int]=None,
        id_max:Optional[int]=None
        ) -> IDRule:
    """
    Compiles an ID rule that retrieves a group ID from a text object field.

    Parameters
    ----------
    regex : str
        DESCRIPTION.
    id_type : IDType
        DESCRIPTION.
    condition : Optional[Callable], optional
        DESCRIPTION. The default is None.
    id_min : Optional[int], optional
        DESCRIPTION. The default is None.
    id_max : Optional[int], optional
        DESCRIPTION. The default is None.

    Returns
    -------
    IDRule
        DESCRIPTION.

    """
    pattern = re.compile(regex)
    
    def function(text: str):
        match = pattern.search(text)
        if not match:
            return None
        return int(match.group(1) if match.lastindex else match.group(0))
    
    def replace(text: str, new_id: int):
        match = pattern.search(text)
        if not match:
            return text
        return text[:match.start(1)] + str(new_id) + text[match.end(1):] if match.lastindex else str(new_id)
    
    optionals = {}
    if condition is not None:
        optionals["condition"] = condition
    if id_min is not None:
        optionals["id_min"] = id_min
    if id_max is not None:
        optionals["id_max"] = id_max
         
    return IDRule(
        obj_prop_id=obj_prop.text.DATA,
        id_type=id_type,
        function=function,
        replace=replace,
        **optionals
    )

ID_SET_BASE = frozenset((
    IDType.GROUP_ID,
    IDType.ITEM_ID,
    IDType.TIME_ID,
    IDType.COLLISION_ID
    ))

ID_SET_REGROUP = frozenset((
    *ID_SET_BASE,
    IDType.CONTROL_ID,
    IDType.REMAP_BASE,
    IDType.REMAP_TARGET
    ))

ID_RULE_TEXT_NUMBER = create_text_id_rule(
    regex=r"^\d+$",
    id_type=IDType.ANY,
    id_min=1,
    id_max=9999
    )
    
ID_RULE_TEXT_ID = create_text_id_rule(
    regex=r"\bID\s+(\d+)\b",
    id_type=IDType.GROUP_ID,
    id_min=1,
    id_max=9999
    )

ID_RULE_REMAP_ID = create_text_id_rule(
    regex=r"^(\d+)\s+[A-Za-z]+",
    id_type=IDType.LABEL
    )

TEXT_RULES = RuleHandler(by_id={obj_id.TEXT:(ID_RULE_TEXT_NUMBER,ID_RULE_TEXT_ID,ID_RULE_REMAP_ID)})

EDITOR_LAYER_RULES = RuleHandler(base=(
    IDRule(obj_prop.EDITOR_L1, IDType.GENERIC, reference=True, default=0, id_min=-32768, id_max=32767),
    IDRule(obj_prop.EDITOR_L2, IDType.GENERIC, reference=True, default=lambda obj: 0 if obj.get(obj_prop.EDITOR_L1) else None, id_min=-32768, id_max=32767)
    ))

ID_RULES_COPY = ID_RULES.compile_rules(id_types=(
    IDType.LINK_ID,
    IDType.KEYFRAME_ID,
    IDType.GRADIENT_ID
    ))

ID_RULES_REGROUP = ID_RULES.compile_rules(id_types=(
    *ID_SET_REGROUP,
    IDType.FORCE_ID,
    IDType.GRADIENT_ID
    ))

ID_RULES_REGROUP_COLOR = ID_RULES.compile_rules(id_types=(
    *ID_SET_REGROUP,
    IDType.COLOR_ID,
    IDType.FORCE_ID,
    IDType.GRADIENT_ID
    ))


def offset_object_ids(
        objects:ObjectList|Level,
        id_offset:Optional[dict]=None,
        ignore_ids:Optional[dict]=None,
        rules:RuleHandler=ID_RULES,
        groups:Optional[Sequence[Sequence[IDType]]]=None
        ):
    
    ignore_ids = ignore_ids or {}
    id_offset = id_offset or {}
    ig_all = ignore_ids.get(IDType.ANY,set())
    io_all = id_offset.get(IDType.ANY,set())
    
    ids = rules.compile_ids(objects, by_type=True, type_groups=groups)
    
    for k,v in ids.items():
        ig = ignore_ids.get(k,set()) | ig_all
        io = id_offset.get(k,io_all)
        old = v.get_ids() - ig
        new = {i + io for i in old}
        kv_map = dict(zip(old,new))
        ids.remap_objects(kv_map)
        
    return objects


def remap_object_ids(
        objects:ObjectList|Level,
        ignore_ids:Optional[dict]=None,
        id_ranges:Optional[dict]=None,
        reassign_all:bool=False,
        override_fixed:bool=False,
        rules:RuleHandler=ID_RULES,
        groups:Optional[Sequence[Sequence[IDType]]]=None
        ):
    
    ignore_ids = ignore_ids or {}
    id_ranges = id_ranges or {}
    ig_all = ignore_ids.get(IDType.ANY,set())
    ir_all = id_ranges.get(IDType.ANY,set())
    
    ids = rules.compile_ids(objects, by_type=True, type_groups=groups)
    
    for k,v in ids.items():
        ig = ignore_ids.get(k,set()) | ig_all
        ir = (id_ranges.get(k,set()) | ir_all) - ig
        used = v.get_ids()
        old = used - ig
        old = {x for x in old if v.vmin <= x <= v.vmax}
        
        range_search = bool(ir)
        
        if range_search:
            range_min = max(v.vmin,min(ir))
            range_max = min(v.vmax,max(ir))
            
            if not reassign_all:
                old -= ir
                ir -= used
            
        else:
            range_min = v.vmin
            range_max = v.vmax
        print("old",old)
        new = next_free(
            ir,
            vmin=range_min,
            vmax=range_max,
            count=len(old),
            in_range=range_search
            )
        kv_map = dict(zip(old,new))
        if k == (IDType.COLOR_ID,):
            print(k,"map",kv_map)
        v.remap_objects(kv_map,override=override_fixed)
        
    return objects


def remap_objects(
        *objects:ObjectList|Level,
        id_func:Callable,
        override_fixed:bool=False,
        ignore_ids:Optional[dict]=None, 
        include_ids:Optional[dict]=None,
        ):
    result = []   
    
    ignore_ids = ignore_ids or {}
    include_ids = include_ids or {}
    ig_all = ignore_ids.get(IDType.ANY,set())
    ic_all = include_ids.get(IDType.ANY,set())
    
    ig_dict = {k: v | ig_all for k,v in ignore_ids.items()}
    ic_dict = {}
    
    for k, v in include_ids.items():
        ic_dict[k] = v | ic_all | ig_dict.get(k,set())
        
    last_ids = {}
    
    for objl in objects:
        objl = copy.deepcopy(objl)
        result.append(objl)
        
        id_map = id_func(objl)
        
        for k,v in id_map.items():
            ic = ic_dict.setdefault(k,set())
            ig = ig_dict.setdefault(k,set())
            ids = v.get("ids")
            av = v.get("values", set())
            tv = v.get("targets", av)
            coll = ic & tv - ig
            
            ic.update(av)
            ic.update(tv)
            
            if coll:
                new = next_free(
                    ic,
                    start=last_ids.get(k),
                    vmin=ids.vmin,
                    vmax=ids.vmax,
                    count=len(coll)
                    )
                if new: last_ids[k] = new[-1]
                kv_map = dict(zip(coll,new))
                ids.remap_objects(kv_map,override=override_fixed)
                ic.update(new)
    
    return result


def remap_objects_copy(*objects:ObjectList|Level):
    
    def id_func(obj_list):
        ids = ID_RULES_COPY.combine_rules(EDITOR_LAYER_RULES).compile_ids(obj_list, by_type=True)
        return {k:{"ids":v,"values":v.get_ids()} for k,v in ids.items()}
    
    return remap_objects(*objects, id_func=id_func)


def remap_objects_regroup(
        *objects:ObjectList|Level, 
        ignore_ids:Optional[dict]=None, 
        include_ids:Optional[dict]=None,
        override_fixed:bool=False,
        rules:RuleHandler=ID_RULES_REGROUP,
        groups:Optional[Sequence[Sequence[IDType]]]=(ID_SET_REGROUP,(IDType.COLOR_ID,)),
        ref_groups:Optional[Sequence[Sequence[IDType]]]=None
        ):
    
    ref_groups = () if ref_groups is None else ref_groups
    
    def id_func(obj_list):
        ids = rules.compile_ids(obj_list, by_type=True,type_groups=groups)
        result = {}
        
        for k,v in ids.items():
            k_ = result.setdefault(k,{})
            
            if k in ref_groups:
                id_base = v.filter_values(reference=False).get_ids()
                id_ref = v.filter_values(reference=True).get_ids()
                av = id_base | id_ref
                tv = id_base & id_ref
                
            else:
                av = v.get_ids()
                tv = av
            
            k_["ids"] = v
            k_["values"] = av
            k_["target"] = tv
            
        return result
        
    return remap_objects(
        *objects, 
        id_func=id_func,
        ignore_ids=ignore_ids,
        include_ids=include_ids,
        override_fixed=override_fixed
        )


def remap_objects_build_helper(
        *objects:ObjectList, 
        ignore_ids:Optional[dict]=None, 
        include_ids:Optional[dict]=None,
        override_fixed:bool=False,
        rules:RuleHandler=ID_RULES_REGROUP,
        groups:Optional[Sequence[Sequence[IDType]]]=(ID_SET_REGROUP,(IDType.COLOR_ID,)),
        ref_groups:Optional[Sequence[Sequence[IDType]]]=None
        ):
    
    ref_groups = groups if ref_groups is None else ref_groups
    
    return remap_objects_regroup(
        *objects,
        ignore_ids=ignore_ids,
        include_ids=include_ids,
        override_fixed=override_fixed,
        rules=rules,
        groups=groups,
        ref_groups=ref_groups        
        )


def combine_objects(*objects:ObjectList):
    objects = remap_objects_copy(*objects)
    
    result = objects[0]
    
    for objl in objects[1:]:
        result.extend(objl)
        
    result.apply(clean_duplicate_groups)
    clean_gid_parents(result)
    
    return result


def combine_levels(*levels:Level):
    levels = remap_objects_copy(*levels)
    
    result = levels[0]
    objs = result.objects
    colors = result.start.get(obj_prop.level.COLORS, ColorList())
    
    for lvl in levels[1:]:
        objs.extend(lvl.objects)
        col = lvl.start.get(obj_prop.level.COLORS)
        if col is not None:  
            colors.add_colors(col)
    
    objs.apply(clean_duplicate_groups)
    clean_gid_parents(objs)
    
    return result
    
    
def objs_from_ids(id_list, condition: Optional[Callable] = None):
    
    seen = set()  
    new = ObjectList()
    
    for i in id_list:
        obj = i.obj
        
        if obj is None:
            continue
        
        obj_str = obj.to_string()
        
        if obj_str in seen: 
            continue
        
        if condition is not None and callable(condition) and not condition(i):
            continue
        
        new.append(obj)
        seen.add(obj_str)
    
    return new


def compile_keyframe_spawn_ids(obj_list:ObjectList):
    
    def key_func(obj):
        spawn_id = obj.get(obj_prop.trigger.keyframe.SPAWN_ID)
        return None if spawn_id == 0 else spawn_id
    
    return compile_keyframe_groups(obj_list,key_func)


def compile_spawn_groups(obj_list:ObjectList):
    
    spawn_groups = { 0: ObjectList() }
    
    for obj in obj_list:
        
        if not obj.get(obj_prop.trigger.SPAWN_TRIGGER):
            continue
        
        if (groups:=obj.get(obj_prop.GROUPS)) is not None:
            
            for i in set(groups):
                spawn_groups.setdefault(i,ObjectList())
                spawn_groups[i].append(obj)
        else:
            spawn_groups[0].append(obj)
    
    for v in spawn_groups.values():
        v.sort(key=lambda obj: obj.get(obj_prop.X))
        
    return spawn_groups


def create_common_group(objects:ObjectList, rules) -> tuple[int]:
    
    common = objects.shared_values(lambda obj: obj.get(obj_prop.GROUPS))
    
    if common:
        return tuple(common)
    
    rules = rules.compile_rules(id_types=(
        *ID_SET_BASE,
        ))
    ids = rules.compile_ids(objects, by_type=False)
    vals = ids.get_ids()
    new = next_free(vals,vmin=ids.vmin,vmax=ids.vmax,count=1)
    add_groups(objects, new)
    return tuple(new)
    

def free_unused_colors(lvl:Level, ignore_ids:dict):
    ignore_ids = ignore_ids or {}
    
    rules = ID_RULES.compile_rules(id_types=(IDType.COLOR_ID,))
    
    ids = rules.compile_ids(lvl.objects, by_type=False).filter_values(fixed=False)
    id_base = ids.filter_values(reference=False).get_ids()
    id_ref = ids.filter_values(reference=True).get_ids()
    unused = id_base - id_ref - ignore_ids
    
    if (colors:=lvl.start.get(obj_prop.level.COLORS)) is not None:        
        lvl.start[obj_prop.level.COLORS] = colors.where(lambda color: color.channel not in unused)


def obj_canon_string(obj:Object):
    d = copy.deepcopy(obj)
    items = sorted(d.items(), key=lambda x: x[0])
    d.clear()
    d.update(items)
    
    return d.to_string()
    
    
def strip_intersection(
        base:ObjectList,
        objects:ObjectList
        ):
    str_set = set(obj_canon_string(obj) for obj in base)
    return objects.where(lambda obj: obj_canon_string(obj) not in str_set)
