# Imports 
import glob
from pathlib import Path
from copy import deepcopy
from typing import Literal
# Package Imports
from gmdkit.mappings import obj_prop, color_prop, color_id
from gmdkit.models.level import Level, LevelList
from gmdkit.functions.object import offset_position
from gmdkit.functions.object_list import boundaries
from gmdkit.functions.remapping import regroup
from gmdkit.functions.color import create_color_triggers

def load_folder(path, extension:str='.gmd') -> LevelList:
    
    level_list = LevelList()
    
    folder_path = str(Path(path) / ('*' + extension))
    files = glob.glob(folder_path)
    
    for file in files:
        print(file)
        level = Level.from_file(file)
        
        level_list.append(level)
    
    
    return level_list


def boundary_offset(level_list:LevelList,vertical_stack:bool=False,block_offset:int=30):
    
    i = None
    
    for level in level_list:
    
        bounds = boundaries(level.objects)
        
        if vertical_stack:
            
            if i == None:
                i = bounds[5]
            
            else:
                level.objects.apply(offset_position, offset_y = i)
                i += bounds[5]-bounds[1] + block_offset * 30
            
        else:
            if i == None:
                i = bounds[4]
            
            else:
                level.objects.apply(offset_position, offset_x = i)
                i += bounds[4]-bounds[0] + block_offset * 30
    
        i = i // 30 * 30


def merge_levels(level_list:LevelList, override_colors:bool=True):
    
    main_level = deepcopy(level_list[0])
    main_colors = main_level.start[obj_prop.level.COLORS]
    main_channels = main_colors.unique_values(lambda color: [color.get(color_prop.CHANNEL)])
        
    for level in level_list[1:]:
        
        main_level.objects += level.objects
        
        colors = level.start[obj_prop.level.COLORS]
        group_colors = colors.get_custom()
        
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


def level_color_triggers(level:Level):
    colors = level.start.get(obj_prop.level.COLORS).where(lambda x: x.get(color_prop.CHANNEL) in color_id.LEVEL)
    level.objects += create_color_triggers(colors)
    
        
    

def regroup_levels(level_list:LevelList, ignored_ids:dict=None, reserved_ids:dict=None, remaps:Literal["none","naive","search"]="none"):
    ignored_ids = ignored_ids or {}
    reserved_ids = reserved_ids or {}
    collisions = reserved_ids
    
    for lvl in level_list:
        #print(collisions)
        objs = [lvl.start] + lvl.objects
        print(regroup(objs, ignored_ids=ignored_ids, reserved_ids=collisions, no_defaults=True))
        print()
        for k, v in objs.id_context.items():
            collisions.setdefault(k,set()).update(v.get_ids())
    
    
    
    