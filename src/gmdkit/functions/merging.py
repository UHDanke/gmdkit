# Imports 
import glob
import math
from pathlib import Path
from typing import Any
from collections.abc import Iterable
from copy import deepcopy
from dataclasses import dataclass
# Package Imports
from gmdkit.mappings import obj_prop, color_prop
from gmdkit.casting.id_rules import ID_RULES, filter_rules
from gmdkit.models.level import Level, LevelList
from gmdkit.models.object import ObjectList, Object
import gmdkit.functions.object as obj_func
import gmdkit.functions.object_list as objlist_func
import gmdkit.functions.level as level_func



RULE_FORMAT = list[dict[str,Any]]

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
    max_limt: int

@dataclass
class IDList:
    values: list
    remappable: list
    

def compile_rules(
        object_id:int, 
        rule_dict:dict[int|str,RULE_FORMAT]=ID_RULES
        ) -> RULE_FORMAT:
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
    
    for oid in ("any", object_id):
        if (val:=rule_dict.get(oid)) is not None:
            rules.extend(val)
            
    return rules

        
def replace_ids(
        obj:Object, 
        key_value_map:dict[str,dict[int,int]],
        rule_dict:dict[int|str,RULE_FORMAT]=ID_RULES
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
        
        pid = rule.get("property_id")
        
        if pid is not None and (val:=obj.get(pid)) is not None:

            if (cond:=rule.get("condition")) and callable(cond) and not cond(obj):
                continue
            
            id_type = rule.get('type','none')
            
            kv_map = key_value_map.get(id_type)
            
            if kv_map is None:
                continue
            
            if (func:=rule.get("replace")) and callable(func):
                func(val, kv_map)
            
            else:
                obj[pid] = kv_map.get(val, val)
                
            
def get_ids(
        obj:Object,
        rule_dict:dict[Any,RULE_FORMAT]=ID_RULES
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

        pid = rule.get("property_id")
        if pid is None: continue
        
        if (val:=obj.get(pid)) is not None or (default:=rule.get("default")) is not None:
            
            if (cond:=rule.get("condition")) and callable(cond) and not cond(obj):
                continue

            if (func:=rule.get("function")) and callable(func):
                val = func(val)
                
            id_type = rule.get('type')
            remappable = rule.get('remappable',False) and obj.get(obj_prop.trigger.SPAWN_TRIGGER,False)
            min_limit = rule.get('min',-2**31)
            max_limit = rule.get('max',2**31-1)
            
            if not rule.get("iterable"): val = val,
            
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
                        id_type = id_type,
                        remappable = remappable,
                        min_limit = min_limit,
                        max_limt = max_limit
                        )


def next_free(
        values:Iterable[int],
        start:int=0,
        vmin:int=-2147483648,
        vmax:int=2147483647,
        count:int=1
        ) -> list[int]:
    """
    Returns the next unused integer from a list, within the given limits.
    Negative numbers are returned counting down from -1.

    Parameters
    ----------
    values : Iterable[int]
        Currently used values.
        
    start : int, optional
        The current next free value, used to speed up iterative searches over large lists. Defaults to 0.
    
    vmin : int, optional
        The minimum value that can be returned. Defaults to -2147483648.
    
    vmax : int, optional
        The maximum value that can be returned. Defaults to 2147483647.
    
    count : int, optional
        The number of values to return. Defaults to 1.
        
    Returns
    -------
    new_ids : list[int]
        A list of ids returned.
    """
    used = set(values)
    result = []

    def range_search(start,stop,step):
        
        nonlocal result
        
        for i in range(start,stop+step,step):
            
            if len(result) > count: 
                break
            
            if i not in used: 
                result.append(i)
    
    if start >= 0:
        range_search(start, vmax, 1)
    
    if start < 0 or len(result) < count: 
        range_search(start, vmin, -1)

    return result
  
    
def compile_ids(ids:Iterable[Identifier()]):
    
    result = {}
    
    for i in ids:

        data = {'list':set(),'remap':set(),'min':i.min_limit,'max':i.max_limit}
        g = result.setdefault(i.id_type,data)
        
        if g['min']<= i.id_val <= g['max']: 
            g['list'].add(i.id_val)
        
        if i.remappable:
            g['remap'].add(i.id_val)

        g['min'] = max(i.min_limit, g['min'])
        g['max'] = min(i.min_limit, g['max'])

    return result



def regroup(
        objects:ObjectList,
        id_context,
        references: Iterable[tuple[int|None,int|None]]:None,
        
        
        
        )

def build_helper():
    
    

def regroup(
        level_list:LevelList,
        ids:Iterable[ID_FORMAT]=ID_LIST,
        ignore_ids:dict[str,Iterable]=IGNORE_IDS, 
        reserved_ids:dict[str,Iterable]=None,
        ignore_spawn_remaps:bool=False,
        remap_all:bool=False
        ):

    seen_ids = {}
    ignore_ids = ignore_ids or {}
    reserved_ids = reserved_ids or {}

    for level in level_list:
        
        all_ids = level.objects.unique_values(get_ids) | set(get_ids(level.start))
        
        compiled = compile_ids(all_ids)
        
        keys = set(compiled.keys())
        
        if keys.intersection(["remap_base","remap_target"]):
            
            if ignore_spawn_remaps:
                keys.difference_update(["remap_base","remap_target"])
            else:
                raise ValueError("Function cannot handle spawn remaps, use 'ignore_spawn_remaps' to ignore them.")
        
        remaps = {}
        
        for k in keys:
            
            v = compiled[k]
            
            seen = seen_ids.get(k,set())
            
            values = v['list']
            collisions = set()
            
            if seen:
                if remap_all:
                    collisions = values
                
                else: collisions = seen & values
            
            
            ignored = set(ignore_ids.get(k,set())) & values
            reserved = set(reserved_ids.get(k,set())) & values
            
            collisions -= ignored
            collisions |= reserved
            
            seen_set = seen_ids.setdefault(k,set())
            seen_set.update(values)
                
            search_space = seen_set | ignored | reserved
            
            
            if collisions:
                
                nxt = next_free(
                    search_space,
                    vmin=v['min'],
                    vmax=v['max'],
                    count=len(collisions)
                    )
                
                remaps[k] = dict(zip(collisions,nxt))
                
                seen_set.update(nxt)
        
        level.objects.apply(replace_ids,key_value_map=remaps)
        replace_ids(level.start,key_value_map=remaps)


def boundary_offset(level_list:LevelList,vertical_stack:bool=False,block_offset:int=30):
    
    i = None
    
    for level in level_list:
    
        bounds = objlist_func.boundaries(level.objects)
        
        if vertical_stack:
            
            if i == None:
                i = bounds[3]
            
            else:
                level.objects.apply(obj_func.offset_position, offset_y = i)
                i += bounds[3]-bounds[1] + block_offset * 30
            
        else:
            if i == None:
                i = bounds[2]
            
            else:
                level.objects.apply(obj_func.offset_position, offset_x = i)
                i += bounds[2]-bounds[0] + block_offset * 30
    
        i = i // 30 * 30


def merge_levels(level_list:LevelList, override_colors:bool=True):
    
    main_level = deepcopy(level_list[0])
    main_colors = main_level.start[obj_prop.level.COLORS]
    main_channels = main_colors.unique_values(lambda color: [color.get(color_prop.CHANNEL)])
        
    for level in level_list[1:]:
        
        main_level.objects += level.objects
        
        colors = level.start[obj_prop.level.COLORS]
        group_colors = colors.where(lambda color: 1 <= color[color_prop.CHANNEL] <= 999)
        
        for color in group_colors:
            color_channel = color.get(color_prop.CHANNEL)
            
            if override_colors:
                if color_channel in main_channels:
                    main_colors[:] = [
                        c for c in main_colors
                        if c.get(color_prop.CHANNEL) != color
                    ]
                
                main_colors.append(color)
                main_channels.add(color_channel)
                
            else:
                if color_channel in main_channels:
                    continue
                else:
                    main_colors.append(color)
                    main_channels.add(color_channel)
    
    return main_level


def load_folder(path, extension:str='.gmd') -> LevelList:
    
    level_list = LevelList()
    
    folder_path = str(Path(path) / ('*' + extension))
    files = glob.glob(folder_path)
    
    for file in files:
        
        level = Level.from_plist(file)
        
        level_list.append(level)
    
    
    return level_list
