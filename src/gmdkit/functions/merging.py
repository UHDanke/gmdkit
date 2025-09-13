# Imports 
import glob
import math
from pathlib import Path
from typing import Any
from collections.abc import Iterable

# Package Imports
from gmdkit.mappings import prop_id, color_id, obj_id, color_prop
from gmdkit.casting.id_rules import ID_RULES, filter_rules
from gmdkit.models.level import Level, LevelList
from gmdkit.models.object import ObjectList, Object
import gmdkit.functions.object as obj_func
import gmdkit.functions.object_list as objlist_func
import gmdkit.functions.level as level_func



ID_FORMAT = tuple[int|str,str,bool,int,int]
RULE_FORMAT = list[dict[str,Any]]

ID_LIST = ["color_id","group_id","item_id","time_id","collision_id","linked_id","gradient_id","effect_id","keyframe_id","unique_sfx_id","sfx_group","force_id","control_id"]

IGNORE_IDS = {
    "effect_id":{0}
    }


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
    
    rules = compile_rules(obj.get(prop_id.id,0),rule_dict=rule_dict)
    
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
        ) -> Iterable[ID_FORMAT]:
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
    id : int
        The found ID value
        
    id_type : str
        The type of ID found (group, collision, item, etc).
        
    is_remappable : bool
        Whether the found ID is potentially remappable.
        
    min_limit : int
        The minimum value to which the ID can be reassigned.  
    
    max_limit : int
        The maximum value to which the ID can be reassigned.
    """
    result = set()

    rules = compile_rules(obj.get(prop_id.id,0),rule_dict=rule_dict)
    
    for rule in rules:

        pid = rule.get("property_id")
        if pid is None: continue
        
        if (val:=obj.get(pid)) is not None or (default:=rule.get("default")) is not None:
            
            if (cond:=rule.get("condition")) and callable(cond) and not cond(obj):
                continue

            if (func:=rule.get("function")) and callable(func):
                val = func(val)
            
            def id_dict(value):
                
                if value is None:
                    if callable(default):
                        value = default(value)
                    elif default is not None:
                        value = default
                
                if value is None:
                    return
                
                data = (
                    value,
                    rule.get('type','none'),
                    (rule.get('remappable',False) and obj.get(prop_id.trigger.spawn_triggered,False)),
                    rule.get('min',-2**31),
                    rule.get('max',2**31-1)
                    )
                
                result.add(data)

            if rule.get("iterable"):
                for v in val:
                    id_dict(v)
                
            else:
                id_dict(val)
                
    yield from result


def next_free(
        values,
        current:int=None,
        vmin:int=None,
        vmax:int=None,
        count:int=1
        ) -> list[int]:
    """
    Returns the next unused integer from a list, within the given limits.
    Positive integers will be returned first, starting from either 0 or vmin up to vmax.
    If no positive integers are available, return negative ones starting from -1 down to vmin.

    Parameters
    ----------
    values : TYPE
        Currently used values.
        
    current : int, optional
        The current next free value, used to speed up iterative searches over large lists. Defaults to None.
    
    vmin : int, optional
        DESCRIPTION. The default is None.
    
    vmax : int, optional
        DESCRIPTION. The default is None.
    
    count : int, optional
        DESCRIPTION. The default is 1.

    Returns
    -------
    new_ids : list
        DESCRIPTION.

    """
    vmin = -math.inf if vmin is None else vmin
    vmax = math.inf if vmax is None else vmax
    
    start = current
           
    if start is None:
        if vmin <= 0 <= vmax:
            start = 0
        elif 0 <= vmin <= vmax:
            start = vmin
        elif vmin <= vmax <= 0:
            start = vmax
    
    if not (vmin <= start <= vmax):
        raise ValueError(f"start index {start} not in range [{vmin},{vmax}]")
        
    candidate = start
    used = set(values)
    result = []
    
    # search positive integers first
    if candidate >= 0:
        while len(result) < count:
            if (vmax is None or candidate <= vmax) and candidate not in used:
                result.append(candidate)
            candidate += 1
            
            if vmax is not None and candidate > vmax:
                break
    
    # search negative integers if no positive ones exist
    if len(result) < count or candidate < 0:
        
        if candidate > 0: candidate = min(vmax,-1)
            
        while len(result) < count:
            if (vmin is None or candidate >= vmin) and candidate not in used:
                result.append(candidate)
            candidate -= 1
            
            if vmin is not None and candidate > vmin:
                break
    
    return result


def compile_ids(ids:Iterable[ID_FORMAT]):
    
    result = {}
    
    for i in ids:
        
        id_val = i[0]
        id_type = i[1]
        is_remappable = i[2]
        id_min = i[3]
        id_max = i[4]
        
        data = {'list':set(),'remap':set(),'min':id_min,'max':id_max}
        g = result.setdefault(id_type,data)
            
        g = result.setdefault(id_type,data)
        
        if g['min']<= id_val <= g['max']: 
            g['list'].add(id_val)
        
        if is_remappable:
            g['remap'].add(id_val)

        g['min'] = max(id_min, g['min'])
        g['max'] = min(id_max, g['max'])

    return result


def regroup(
        level_list:LevelList,
        ids:Iterable[ID_FORMAT]=ID_LIST,
        ignore_ids:dict[str,Iterable]=IGNORE_IDS, 
        reserved_ids:dict[str,Iterable]=None,
        ignore_spawn_remaps:bool=False,
        remap_all:bool=False
        ):
    """
    

    Parameters
    ----------
    level_list : LevelList
        DESCRIPTION.
    ids : ID_FORMAT, optional
        DESCRIPTION. The default is ID_LIST.
    ignore_ids : dict[str,Iterable], optional
        DESCRIPTION. The default is IGNORE_IDS.
    reserved_ids : dict[str,Iterable], optional
        DESCRIPTION. The default is None.
    ignore_spawn_remaps : bool, optional
        DESCRIPTION. The default is False.

    Raises
    ------
    ValueError
        DESCRIPTION.

    Returns
    -------
    None.

    """

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


def combine_levels(level_list:LevelList, override_colors:bool=True):
    
    main_level = level_list[0]
    main_colors = main_level.start[prop_id.level.colors]
    main_channels = main_colors.unique_values(lambda color: [color.get(color_prop.channel)])

    def delete_color(color_id):
        nonlocal main_colors
        main_colors[:] = [
            color for color in main_colors
            if color.get(color_prop.channel) != color_id
        ]
        
        
    for level in level_list[1:]:
        
        main_level.objects += level.objects
        
        colors = level.start[prop_id.level.colors]
        group_colors = colors.where(lambda color: 1 <= color[color_prop.channel] <= 999)
        
        for color in group_colors:
            color_channel = color.get(color_prop.channel)
            
            if override_colors:
                if color_channel in main_channels:
                    delete_color(color)
                
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
