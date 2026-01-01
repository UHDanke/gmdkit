# Imports
from typing import Any, Literal
from collections.abc import Callable
from collections.abc import Iterable
from dataclasses import dataclass

# Package Imports
from gmdkit.mappings import obj_prop, obj_id
from gmdkit.models.object import ObjectList, Object
from gmdkit.casting.id_rules import ID_RULES, IDRule
from gmdkit.functions.misc import next_free
from gmdkit.functions.object_list import compile_keyframe_groups


@dataclass(frozen=True)
class Identifier:
    obj_id: int
    obj_prop: int
    id_val: int
    id_type: str
    remappable: bool
    min_limit: int
    max_limit: int
    reference: bool
    default: bool
    fixed: bool
    

def compile_rules(
        object_id:int, 
        rule_dict:dict[int|str,list[IDRule]]=ID_RULES
        ) -> list[IDRule]:
    """
    Compiles a set of rules by object ID.

    Parameters
    ----------
    object_id : int
        The object id for which to return rules.
        
    rule_dict : dict[int|str,RULE_FORMAT], optional
        A dictionary containing rules used to compile IDs. Defaults to ID_RULES.

    Returns
    -------
    rules : RULE_FORMAT
        The compiled rules for the given ID.
    """
    rules = list()
    
    for oid in (None, object_id):
        if (val:=rule_dict.get(oid)) is not None:
            rules.extend(val)
            
    return rules

  
    
def get_ids(
        obj:Object,
        rule_dict:dict[Any,list[IDRule]]=ID_RULES
        ) -> Iterable[Identifier]:
    """
    Compiles unique ID data referenced by an object.

    Parameters
    ----------
    obj : Object
        The object to search for IDs.
        
    rule_dict : dict
        A dictionary containing rules used to compile IDs.
        
    Yields
    ------
    id : Identifier
        A read-only class containing info about the ID.
    """
    oid = obj.get(obj_prop.ID,0)
    
    rules = compile_rules(oid,rule_dict=rule_dict)
    
    for rule in rules:

        pid = rule.prop
        
        if (val:=obj.get(pid)) is not None or rule.fallback is not None or rule.default is not None:
            
            if (cond:=rule.condition) and callable(cond) and not cond(obj):
                continue

            if (func:=rule.function) and callable(func):
                val = func(val)
            
            if not val and val is not False:
                # object id fallback
                if callable(rule.fallback):
                    val = rule.fallback(obj)

            if not rule.iterable: val = val,
            
            for v in val:
                default = rule.get_value("default", obj)
                
                if v is None: v = default
                if v is None: continue
                    
                yield Identifier(
                        obj_id = oid,
                        obj_prop = pid,
                        id_val = v,
                        id_type = rule.type,
                        remappable = rule.remappable and obj.get(obj_prop.trigger.SPAWN_TRIGGER, False),
                        reference = rule.reference,
                        min_limit = rule.min,
                        max_limit = rule.max,
                        default = v==default,
                        fixed = rule.get_value("fixed", v) or v==default
                        )
 

def replace_ids(
        obj:Object, 
        key_value_map:dict[str,dict[int,int]],
        rule_dict:dict[int|str,list[IDRule]]=ID_RULES
        ) -> None:
    """
    Remaps an object's IDs to new values.

    Parameters
    ----------
    obj : Object
        The object to modify.
        
    key_value_map : dict[str,dict[int,int]]
        A dictionary mapping ID types to dictionaries mapping old to new values.
        
    rule_dict : dict[int|str,RULE_FORMAT], optional
        dictionary containing rules used to replace IDs. Defaults to ID_RULES.

    Returns
    -------
    None
    

    """
    
    rules = compile_rules(obj.get(obj_prop.ID,0),rule_dict=rule_dict)
    
    for rule in rules:
        
        pid = rule.prop
        
        if (val:=obj.get(rule.prop)) is not None or rule.fallback is not None or rule.default is not None:

            if (cond:=rule.condition) and callable(cond) and not cond(obj):
                continue
            
            
            kv_map = key_value_map.get(rule.type)

            if kv_map is None: continue
            
            if not val and val is not False:
                # object id fallback
                if callable(rule.fallback):
                    val = rule.fallback(obj)

            if rule.fixed: continue            

            if rule.default is not None:
                if val is None:
                    continue
                if callable(rule.default) and val == rule.default(obj):
                    continue
                if val == rule.default:
                    continue

            if (func:=rule.replace) and callable(func):
                func(val, kv_map)
            
            elif (new:=kv_map.get(val)) is not None:
                obj[pid] = new

                


class IDType:

    
    def __init__(self):
        self.ids = set()
        self.ignored = set()
        self.remaps = dict()
        self.min = -2147483648
        self.max = 2147483647
    
    
    def get_ids(
        self,
        remappable:bool = None,
        reference:bool = None,
        remap:bool = None,
        default:bool = None,
        fixed:bool = None,
        in_range:bool = False,
    ) -> set[int]:

        result = set()
        for i in self.ids:
            
            if in_range and not self.min <= i.id_val <= self.max:
                continue
            
            if default is not None and i.default != default:
                continue
            
            if fixed is not None and i.fixed != fixed:
                continue
            
            if remappable is not None and i.remappable != remappable:
                continue

            if reference is not None and i.reference != reference:
                continue
            
            if remap and i.remappable:
                result.update(self.remaps.get(i.id_val,set()))
            
            result.add(i.id_val)
                
        return result
    
    
    def get_limits(self):
        self.min = -2147483648
        self.max = 2147483647
        for i in self.ids:
            self.min = max(i.min_limit, self.min)
            self.max = min(i.max_limit, self.max)
        
        return self.min, self.max
    
    
    def add_remaps(self, remaps:dict):
        
        for k,l in remaps.items():                
            group = self.remaps.setdefault(k,set())
            group.update(set(l))

   
def compile_ids(ids:Iterable[Identifier]):
    
    result = {}
    
    for i in ids:
        group = result.setdefault(i.id_type, IDType())  
        group.ids.add(i)
                
    return result

def compile_remap_ids(obj_list:ObjectList) -> dict[int,dict[int,int]]:
    
    remaps = {}
    ids = set()
    
    i = 1
    
    for obj in obj_list:
        if obj.get(obj_prop.ID) != obj_id.trigger.SPAWN:
            continue
        if (r:=obj.get(obj_prop.trigger.spawn.REMAPS)):
            remaps[i] = r.to_dict()
            remap_id = i
            i+=1
        else:
            remap_id = 0
        
        identif = Identifier(
            obj_id=obj_id.trigger.SPAWN,
            obj_prop=None,
            id_val=remap_id,
            id_type="remap_id",
            remappable=obj.get(obj_prop.trigger.SPAWN_TRIGGER, False),
            min_limit=0,
            max_limit=2147483647,
            reference=True,
            default=remap_id==0,
            fixed=False
            )
        obj.spawn_remap_id = remap_id
        ids.add(identif)
        
    obj_list.remaps = remaps
    return ids


def compile_keyframe_spawn_ids(obj_list:ObjectList):
    
    func = lambda obj: obj.get(obj_prop.trigger.keyframe.SPAWN_ID, 0)
    
    return compile_keyframe_groups(obj_list,func)


def compile_spawn_groups(obj_list:ObjectList):
    
    spawn_groups = { 0: ObjectList() }
    
    for obj in obj_list:
        if not obj.get(obj_prop.trigger.SPAWN_TRIGGER):
            continue
        if (groups:=obj.get(obj_prop.GROUPS)):
            
            for i in set(groups):
                spawn_groups.setdefault(i,ObjectList())
                spawn_groups[i].add(obj)
        else:
            spawn_groups[0].add(obj)
        
    return spawn_groups


def compile_id_context(obj_list:ObjectList, extra_ids:set()=None, remaps:Literal["none","naive","search"]="none"):
    id_list = obj_list.unique_values(get_ids)
    if extra_ids: id_list.update(extra_ids)
    id_list.update(compile_remap_ids(obj_list))
    compiled = compile_ids(id_list)
    
    match remaps:
        # ignore remapped ids
        case "none":
            pass
        # naive approach, assumes if an ID can get remapped, it will get remapped
        case "naive":
            remap_id_map = {}
            for _, rd in obj_list.remaps.items():
                for old, new in rd.items():
                    remap_id_map.setdefault(old,set()).add(new)
                
            remaps = compiled.get('remap_base',{}).get_ids()
    
            if remaps: 
                for k, d in compiled.items():
                    remappable = d.get_ids(remappable=True)
                    if remappable:
                        d.add_remaps({k: remap_id_map[k] for k in remaps & remappable})
                        
    obj_list.id_context = compiled
    return compiled


def regroup(
        obj_list,
        min_ids:dict=None,
        max_ids:dict=None,
        ignored_ids:dict=None,
        reserved_ids:dict=None,
        remaps:Literal["none","naive","search"]="none"
        ):
    
    min_ids = min_ids or {}
    max_ids = max_ids or {}
    ignored_ids = ignored_ids or {}
    reserved_ids = reserved_ids or {}
    
    ids = compile_id_context(obj_list,remaps=remaps)
    new_remaps = {}
    
    for k, v in ids.items():        
        values = v.get_ids(default=False,fixed=False)
        id_min, id_max = v.get_limits()
        low = max(min_ids.get(k, id_min),id_min)
        high = min(max_ids.get(k, id_max),id_max)
        
        ignored = set(ignored_ids.get(k,set())) & values
        reserved = set(reserved_ids.get(k,set())) & values
        collisions = set(filter(lambda x: not (low <= x <= high), values))
        collisions -= ignored
        collisions |= reserved
        if collisions:
            new_ids = next_free(
                v.get_ids(),
                vmin=low,
                vmax=high,
                count=len(collisions)
                )
            new_remaps[k] = dict(zip(collisions,new_ids))
    obj_list.apply(replace_ids,key_value_map=new_remaps)
    compile_id_context(obj_list,remaps=remaps)
    return new_remaps


def remap_text_ids(obj_list:ObjectList, filter_func:Callable=None, regex_pattern:str=r"^(?:ID\s+(\d+)|(\d+)\s+(.+))$"):
    
    objs = obj_list.where(lambda obj: obj.get(obj_prop.ID)==obj_id.TEXT)
    
    if filter_func and callable(filter_func):
        objs = objs.where(filter_func)
    
    if objs:
        pass
            
    return

# compile all ids
# compile remaps
# if remaps:
#   compile spawn groups
#   compile ids per spawn group
#   filter only remappable
#   compile spawns per group
#   compile keyframe per anim id
#   compile timers & time events
#   

def clean_remaps(objs:ObjectList) -> None:
    """
    Cleans remaps with keys assigned to multiple values. 
    While this is allowed by the game and the remaps are serialized as lists and not as dictionaries, remap keys are unique and only the last key-value pair is used in remap logic.

    Parameters
    ----------
    objs : ObjectList
        The objects to modify.

    Returns
    -------
    None.

    """
    for obj in objs:
        if obj.get(obj_prop.ID) == obj_id.trigger.SPAWN and (remaps:=obj.get(obj_prop.trigger.spawn.REMAPS)) is not None:
            remaps.clean()
        
        
