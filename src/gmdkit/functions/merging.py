# Imports 
import glob
from pathlib import Path
from copy import deepcopy
from typing import Literal
# Package Imports
from gmdkit.mappings import obj_prop, obj_id, color_prop, color_id
from gmdkit.models.object import Object, ObjectList
from gmdkit.functions.object_list import boundaries, add_groups
from gmdkit.models.level import Level, LevelList
from gmdkit.functions.object import offset_position
from gmdkit.functions.remapping import regroup, compile_id_context
from gmdkit.functions.color import create_color_triggers
from gmdkit.functions.misc import next_free

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


def disable_start_pos(obj):
    if obj.get(obj_prop.ID)!=obj_id.trigger.START_POSITION:
        return
    obj[obj_prop.start_pos.DISABLE] = False


def level_color_triggers(level:Level):
    colors = level.start.get(obj_prop.level.COLORS).where(lambda x: x.get(color_prop.CHANNEL) in color_id.LEVEL)
    level.objects += create_color_triggers(colors)


def obj_list_group(obj_list):
    ids = compile_id_context(obj_list)
    g, = next_free(values=ids["group_id"].get_ids(),vmin=1,vmax=9999,count=1)
    add_groups(obj_list,{g})
    return g,

def level_add_toggles(lvl_list:LevelList):
    init_toggles = ObjectList()
    Y = 0
    for lvl in lvl_list:
        obj_list = [lvl.start] + lvl.objects 
        min_x, min_y, center_x, center_y, max_x, max_y = boundaries(obj_list)
        g = obj_list_group(obj_list)
        
        init_toggle = Object.default(obj_id.trigger.TOGGLE)
        init_toggle.update(
            {
                obj_prop.X: 0,
                obj_prop.Y: 15+Y,
                obj_prop.trigger.toggle.GROUP_ID: g,          
                }
            )
        obj_list.append(init_toggle)
        init_toggles.append(init_toggle)
        
        start_toggle = Object.default(obj_id.trigger.TOGGLE)
        start_toggle.update(
            {
                obj_prop.X: min_x,
                obj_prop.Y: 15,
                obj_prop.trigger.toggle.GROUP_ID: g,
                obj_prop.trigger.toggle.ACTIVATE_GROUP: True            
                }
            )
        obj_list.append(start_toggle)
        
        end_toggle = Object.default(obj_id.trigger.TOGGLE)
        end_toggle.update(
            {
                obj_prop.X: max_x,
                obj_prop.Y: 15,
                obj_prop.trigger.toggle.GROUP_ID: g,     
                }
            )
        obj_list.append(end_toggle)
        Y -= 30
        
    return init_toggles

def regroup_levels(level_list:LevelList, ignored_ids:dict=None, reserved_ids:dict=None, remaps:Literal["none","naive","search"]="none"):
    ignored_ids = ignored_ids or {}
    reserved_ids = reserved_ids or {}
    collisions = reserved_ids
    
    for lvl in level_list:
        #print(collisions)
        objs = [lvl.start] + lvl.objects
        regroup(objs, ignored_ids=ignored_ids, reserved_ids=collisions)
        for k, v in objs.id_context.items():
            
            collisions.setdefault(k,set()).update(v.get_ids())
    