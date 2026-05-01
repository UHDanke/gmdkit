# Imports
import copy
from typing import Callable, Optional
import re

# Package Imports
from gmdkit.casting.id_rules import ID_RULES
from gmdkit.other.id_classes import IDType, IDRule, RuleHandler
from gmdkit import Level
from gmdkit.mappings import obj_prop, obj_id
from gmdkit.models.object import ObjectList
from gmdkit.utils.misc import next_free
from gmdkit.functions.object import clean_duplicate_groups
from gmdkit.functions.object_list import compile_keyframe_groups, clean_gid_parents 

ID_SET_BASE = (
    IDType.GROUP_ID,
    IDType.ITEM_ID,
    IDType.TIME_ID,
    IDType.COLLISION_ID
    )

ID_SET_REGROUP = (
    *ID_SET_BASE,
    IDType.CONTROL_ID,
    IDType.REMAP_BASE,
    IDType.REMAP_TARGET
    )


def create_text_id_rule(
        regex:str,
        id_type:IDType,
        condition:Optional[Callable]=None,
        id_min:Optional[int]=None,
        id_max:Optional[int]=None
        ):
    
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


def combine_objects(*objects:ObjectList, id_func:Callable):
    result = ObjectList()
    id_dict = {}
    last_ids = {}
    
    for objl in objects:
        objl_copy = copy.deepcopy(objl)
        result.extend(objl_copy)
        
        id_map = id_func(objl_copy)
        
        for k,v in id_map.items():
            vals = id_dict.setdefault(k,set())
            ids = v["ids"]
            av = v.get("values")
            tv = v.get("targets",av)
            coll = vals & tv
            
            if coll:
                new = next_free(vals,start=last_ids.get(k),vmin=ids.vmin,vmax=ids.vmax,count=len(coll))
                if new:
                    last_ids[k] = new[-1]
                kv_map = dict(zip(coll,new))
                ids.remap_objects(kv_map)
                vals.update(new)
                
            vals.update(av)
    
    return result


def combine_objects_copy(*objects:ObjectList):
    
    rules = ID_RULES.compile_rules(id_types=(
        IDType.LINK_ID,
        IDType.KEYFRAME_ID,
        ))

    def id_func(obj_list):
        ids = rules.compile_ids(obj_list, by_type=True)
        return {k:{"ids":v,"values":v.get_ids()} for k,v in ids.items()}
    
    result = combine_objects(*objects, id_func=id_func)
    clean_gid_parents(result)
    
    return result


def combine_objects_regroup(
        *objects:ObjectList, 
        ignore_ids:Optional[dict]=None, 
        include_ids:Optional[dict]=None,
        rules:RuleHandler=ID_RULES
        ):
    
    ignore_ids = ignore_ids or {}
    include_ids = include_ids or {}
    
    groups = (ID_SET_REGROUP,)
    rules = rules.compile_rules(id_types=(
        *ID_SET_REGROUP,
        IDType.LINK_ID,
        IDType.KEYFRAME_ID
        ))
    
    def id_func(obj_list):
        ids = rules.compile_ids(obj_list, by_type=True,type_groups=groups)
        result = {}
        
        for k,v in ids.items():
            k_ = result.setdefault(k,{})
            vals = v.get_ids()
            ig = ignore_ids.get(k,set())
            ic = include_ids.get(k,set())
            k_["ids"] = v
            k_["values"] = vals
            k_["target"] = (vals - ig) | ic
            
        return result
    
    result = combine_objects(*objects, id_func=id_func)
    result.apply(clean_duplicate_groups)
    clean_gid_parents(result)
    
    return result


def combine_objects_build_helper(
        *objects:ObjectList, 
        ignore_ids:Optional[dict]=None, 
        include_ids:Optional[dict]=None,
        rules:RuleHandler=ID_RULES
        ):
    
    ignore_ids = ignore_ids or {}
    include_ids = include_ids or {}
    
    groups = (ID_SET_REGROUP,)
    rules = rules.compile_rules(id_types=(
        *ID_SET_REGROUP,
        IDType.LINK_ID,
        IDType.KEYFRAME_ID
        ))
    
    def id_func(obj_list):
        ids = rules.compile_ids(obj_list, by_type=True,type_groups=groups)
        result = {}
        
        ids_regroup = ids.pop(ID_SET_REGROUP)
        id_base = ids_regroup.filter_values(reference=False).get_ids()
        id_ref = ids_regroup.filter_values(reference=True).get_ids()
        k_ = result.setdefault(ID_SET_REGROUP, {})
        ig = ignore_ids.get(ID_SET_REGROUP,set())
        ic = include_ids.get(ID_SET_REGROUP,set())
        k_["ids"] = ids_regroup
        k_["values"] = id_base | id_ref
        k_["target"] = (id_base & id_ref - ig) | ic
        
        for k,v in ids.items():
            k_ = result.setdefault(k,{})
            vals = v.get_ids()
            ig = ignore_ids.get(k,set())
            ic = include_ids.get(k,set())
            k_["ids"] = v
            k_["values"] = vals
            k_["target"] = (vals - ig) | ic
            
        return result
    
    result = combine_objects(*objects, id_func=id_func)
    result.apply(clean_duplicate_groups)
    clean_gid_parents(result)
    
    return result


def objs_from_ids(id_list, condition: Optional[Callable] = None):
    new = ObjectList()
    
    for i in id_list:
        obj = i.obj
        
        if obj is None: continue
        if obj in new: continue
        
        if condition is not None and callable(condition) and not condition(i):
            continue
        
        new.append(obj)
    
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