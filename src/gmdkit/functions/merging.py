# Imports 
import glob
import math
from pathlib import Path
from typing import Any, Callable
from collections.abc import Iterable
from copy import deepcopy
from dataclasses import dataclass
# Package Imports
from gmdkit.mappings import obj_prop, color_prop
from gmdkit.casting.id_rules import ID_RULES, IDRule, ID_TYPES
from gmdkit.models.level import Level, LevelList
from gmdkit.models.object import ObjectList, Object
import gmdkit.functions.object as func_obj
import gmdkit.functions.object_list as func_objlist
import gmdkit.functions.level as func_level




def compile_ids(ids:Iterable[Identifier], filter_limit:bool=False, filter_condition:Callable=None):
    
    result = {}
    
    for i in ids:
        
        if filter_condition is not None and callable(filter_condition) and filter_condition(i):
            continue
        
        group = result.setdefault(i.id_type, {})        
        group.setdefault('values',set())
        group.setdefault('remappable',set())
        group.setdefault('references',set())
        group.setdefault('min',i.min_limit)
        group.setdefault('max',i.max_limit)

        group['values'].add(i.id_val)
        
        if i.remappable:
            group['remappable'].add(i.id_val)
            
        if i.references:
            group['references'].add(i.id_val)

        group['min'] = max(i.min_limit, group['min'])
        group['max'] = min(i.min_limit, group['max'])
    
    
    if filter_limit:
        for id_type, group in result.items():
            for key in ['values','remappable']:
                group[key] = {v for v in group[key] if group['min'] < v < group['max']}
            
    return result


def regroup(
        level_list:LevelList,
        ids:Iterable=ID_TYPES,
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
            
            values = v['values']
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


def offset_ids(level:Level(),offset_all:int=0, offset_map:dict=None):
    
    offset_map = offset_map or {}
    
    all_ids = level.objects.unique_values(get_ids)
    #print(all_ids)
    compiled = compile_ids(all_ids)
    keys = set(compiled.keys())
    
    remaps = {}
    
    for k in keys:
        offset = offset_all + offset_map.get(k, 0)
        
        id_list = compiled[k]["values"]
        remaps[k] = {i: i + offset for i in compiled[k]["values"] if i != 0 and offset != 0}
    print(remaps)
    level.objects.apply(replace_ids,key_value_map=remaps)

def boundary_offset(level_list:LevelList,vertical_stack:bool=False,block_offset:int=30):
    
    i = None
    
    for level in level_list:
    
        bounds = func_objlist.boundaries(level.objects)
        
        if vertical_stack:
            
            if i == None:
                i = bounds[5]
            
            else:
                level.objects.apply(func_obj.offset_position, offset_y = i)
                i += bounds[5]-bounds[1] + block_offset * 30
            
        else:
            if i == None:
                i = bounds[4]
            
            else:
                level.objects.apply(func_obj.offset_position, offset_x = i)
                i += bounds[4]-bounds[0] + block_offset * 30
    
        i = i // 30 * 30


def merge_levels(level_list:LevelList, override_colors:bool=True):
    
    main_level = deepcopy(level_list[0])
    main_colors = main_level.start[obj_prop.level.COLORS]
    main_channels = main_colors.unique_values(lambda color: [color.get(color_prop.CHANNEL)])
        
    for level in level_list[1:]:
        
        main_level.objects += level.objects
        
        colors = level.start[obj_prop.level.COLORS]
        group_colors = colors.where(lambda color: 1 <= color.get(color_prop.CHANNEL,0) <= 999)
        
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
        print(file)
        level = Level.from_file(file)
        
        level_list.append(level)
    
    
    return level_list
