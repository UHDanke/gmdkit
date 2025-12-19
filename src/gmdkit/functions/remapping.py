# Imports
from typing import Any, Literal
from collections.abc import Callable
from statistics import mean, median

# Package Imports
from gmdkit.mappings import obj_prop, obj_id
from gmdkit.models.object import ObjectList, Object

def index_objects(obj_list:ObjectList, index_key:int|str=0, start:int=0) -> None:
    """
    Adds an index key to all objects in the list.
    Useful for tracking the load order of an object or for identifying a particular object when using compilation tools.
    This index is discarded upon loading and saving the level in-game.
    
    Parameters
    ----------
    obj_list : ObjectList
        The objects to modify.
        
    index_key : int | str, optional
        The index key used. Defaults to 0.
        Preferably keep as 0 or use an alphanumeric string key. There isn't an unused'
        
    start : TYPE, optional
        The value to start indexing from. Defaults to 0.

    Returns
    -------
    None.

    """
    for i, obj in enumerate(obj_list, start=start):
        
        obj[index_key] = i
        

def compile_remaps(objs:ObjectList) -> dict[int,dict[int,int]]:
    
    remaps = {}
    
    i = 1
    
    for obj in objs:
        if obj.get(obj_prop.ID) != obj_id.trigger.SPAWN:
            continue
        if (r:=obj.get(obj_prop.trigger.spawn.REMAPS)):
            remaps[i] = r.to_dict()
            obj["remap_id"] = i
            i+=1
        else:
            obj["remap_id"] = 0

    return remaps


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
        
        
