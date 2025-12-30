# Imports
from typing import Any, Literal
from collections.abc import Callable
from statistics import mean, median
from collections.abc import Iterable
from dataclasses import dataclass

# Package Imports
from gmdkit.mappings import obj_prop, obj_id
from gmdkit.models.object import ObjectList, Object
from gmdkit.casting.id_rules import ID_RULES, IDRule
import gmdkit.functions as gmdfunc


IGNORE_IDS = {
    "effect_id":{0}
    }


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

@dataclass
class IDList:
    values: list
    remappable: list
    

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
        
        if (val:=obj.get(rule.prop)) is not None:

            if (cond:=rule.condition) and callable(cond) and not cond(obj):
                continue
                        
            kv_map = key_value_map.get(rule.type)

            if kv_map is None: continue
            
            if (func:=rule.replace) and callable(func):
                func(val, kv_map)
            
            else:
                obj[pid] = kv_map.get(val, val)
                
            
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
        
        if (val:=obj.get(pid)) is not None or (default:=rule.default) is not None:
            
            if (cond:=rule.condition) and callable(cond) and not cond(obj):
                continue

            if (func:=rule.function) and callable(func):
                val = func(val)
                
            id_type = rule.type
            remappable = rule.remappable and obj.get(obj_prop.trigger.SPAWN_TRIGGER, False)
            reference = rule.reference
            min_limit = rule.min
            max_limit = rule.max
            
            if not rule.iterable: val = val,
            
            for v in val:
                
                if v is None:
                    if callable(default):
                         v = default(v)
                    elif default is not None:
                        v = default
                
                if v is None: continue
                
                yield Identifier(
                        obj_id = oid,
                        obj_prop = pid,
                        id_val = v,
                        id_type = id_type,
                        remappable = remappable,
                        reference = reference,
                        min_limit = min_limit,
                        max_limit = max_limit
                        )
 
    
def compile_ids(ids:Iterable[Identifier], filter_limit:bool=False, filter_condition:Callable=None):
    
    result = {}
    
    for i in ids:
        
        if filter_condition is not None and callable(filter_condition) and filter_condition(i):
            continue
        
        group = result.setdefault(i.id_type, {})        
        group.setdefault('values',set())
        group.setdefault('remappable',set())
        group.setdefault('reference',set())
        group.setdefault('min',i.min_limit)
        group.setdefault('max',i.max_limit)

        group['values'].add(i.id_val)
        
        if i.remappable:
            group['remappable'].add(i.id_val)
            
        if i.reference:
            group['reference'].add(i.id_val)

        group['min'] = max(i.min_limit, group['min'])
        group['max'] = min(i.max_limit, group['max'])
    
    
    if filter_limit:
        for id_type, group in result.items():
            for key in ['values','remappable','reference']:
                group[key] = {v for v in group[key] if group['min'] < v < group['max']}
            
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
            reference=True
            )
        obj.spawn_remap_id = remap_id
        ids.add(identif)
        
    obj_list.remaps = remaps
    return ids


def compile_keyframe_spawn_ids(obj_list:ObjectList):
    
    func = lambda obj: obj.get(obj_prop.trigger.keyframe.SPAWN_ID, 0)
    
    return gmdfunc.object_list.compile_keyframe_groups(obj_list,func)


SPAWN_TRIGGERS = []


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

def compile_object_ids(obj_list:ObjectList, extra_ids):
    id_list = obj_list.unique_values(get_ids)
    id_list.update(extra_ids)
    id_list.update(compile_remap_ids(obj_list))
    compiled = compile_ids(id_list)
    return compiled
    

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

def compile_groups(obj_list:ObjectList):
    
    
    return
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
        
        
