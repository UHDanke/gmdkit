# Imports
import math
from typing import Any

# Package Imports
from gmdkit.models.object import Object
from gmdkit.mappings import color_id, prop_id, obj_id
    

def clean_duplicate_groups(obj:Object) -> None:
    """
    Removes duplicate groups from an object. 
    Duplicate groups may multiply the effects of a trigger on an object.

    Parameters
    ----------
    obj : Object
        The object to modify.

    Returns
    -------
    None.

    """
    if (groups:=obj.get(prop_id.groups)) is not None:
        
        obj[prop_id.groups][:] = set(groups)


def clean_remaps(obj:Object) -> None:
    """
    Cleans remaps with keys assigned to multiple values. 
    While this is allowed by the game and the remaps are serialized as lists and not as dictionaries, remap keys are unique and only the last key-value pair is used in remap logic.

    Parameters
    ----------
    obj : Object
        The object to modify.

    Returns
    -------
    None.

    """    
    if obj.get(prop_id.id) == obj_id.trigger.spawn and (remaps:=obj.get(prop_id.trigger.spawn.remaps)) is not None:
        remaps.clean()

def recolor_shaders(obj:Object) -> None:
    """
    Makes shader triggers use white color instead of object outline.

    Parameters
    ----------
    obj : Object
        The object to modify.

    Returns
    -------
    None.

    """
    shader_triggers = [2904,2905,2907,2909,2910,2911,2912,2913,2914,2915,2916,2917,2919,2920,2921,2922,2923,2924]
    
    if obj.get(prop_id.id) in shader_triggers:
        
        if prop_id.color_1 not in obj:
            
            obj[prop_id.color_1] = color_id.white



def fix_lighter(obj:Object, replacement:int=color_id.white) -> None:
    """
    Replaces the base lighter color of an object (which crashes the game) with another color.

    Parameters
    ----------
    obj : Object
        The object to modify.
    replacement : int, optional
        DESCRIPTION. Defaults to white.

    Returns
    -------
    None.

    """
    if obj.get(prop_id.color_1) == color_id.lighter:
        
        obj[prop_id.color_1] = replacement
    

def pop_zeros(obj:Object) -> None:
    """
    Removes object properties with value 0 in-place.

    Parameters
    ----------
    obj : Object
        The object to modify.

    Returns
    -------
    None.

    """
    for key, value in obj.items():
        
        if value == 0:
            obj.pop(key)
            
  
def offset_position(
        obj:Object,
        offset_x:float=0,
        offset_y:float=0
        ) -> None:
    """
    Offsets the position of an object.

    Parameters
    ----------
    obj : Object
        The object for which to offset the position.
    offset_x : float, optional
        The horizontal offset. Default to 0.
    offset_y : float, optional
        The vertical offset. Defaults to 0.

    Returns
    -------
    None.

    """
    if obj.get(prop_id.x) is not None:
        obj[prop_id.x] += offset_x
        
    if obj.get(prop_id.y) is not None:
        obj[prop_id.y] += offset_y


def scale_position(
        obj:Object,
        scale_x:float=1.00,scale_y:float=1.00,
        center_x:float=None, center_y:float=None, 
        only_move:bool=False
        ) -> None:
    
    if not only_move:
        obj[prop_id.scale_x] = obj.get(prop_id.scale_x, 1.00) * scale_x
        obj[prop_id.scale_y] = obj.get(prop_id.scale_y, 1.00) * scale_y
    
    if center_x is not None and (x:=obj.get(prop_id.x)) is not None:
        obj[prop_id.x] = scale_x * (x - center_x)
     
    if center_y is not None and (x:=obj.get(prop_id.x)) is not None:
        obj[prop_id.y] = scale_y * (y - center_y)


def rotate_position(
        obj:Object,
        angle:float=0, 
        center_x:float=None, center_y:float=None, 
        only_move:bool=False
        ):
    
    if not only_move:
        skew_x = obj.get(prop_id.skew_x)
        skew_y = obj.get(prop_id.skew_y)
        
        if skew_x is None and skew_y is None:
            obj[prop_id.rotation] = obj.get(prop_id.rotation,0) + angle
        
        else:
            obj[prop_id.skew_x] = skew_x or 0 + angle
            obj[prop_id.skew_y] = skew_y or 0 + angle

    if (
            center_x is not None and center_y is not None 
            and (x:=obj.get(prop_id.x)) is not None 
            and (y:=obj.get(prop_id.y)) is not None
            ):
        th = math.radians(angle)

        dx = x - center_x
        dy = y - center_y

        obj[prop_id.x] = dx * math.cos(th) - dy * math.sin(th)
        obj[prop_id.y] = dx * math.sin(th) + dy * math.cos(th)


def remap_keys(obj:Object, keys:int|str, value_map:dict[Any,Any]):
    
    for key in set(keys) & obj.keys():
    
        obj[key] = value_map.get(obj[key], obj[key])


    
def delete_keys(obj:Object, keys:int|str):
    
    for key in set(keys) & obj.keys():
        
        obj.pop(key)
                  
            
def to_user_coins(obj:Object) -> None:
    
    if obj.get(prop_id.id) == 142:
        
        obj[prop_id.id] = obj_id.collectible.user_coin
        
        obj.pop(prop_id.trigger.collectible.coin.coin_id, None)


def fix_transform(obj) -> None:

    if (scale_x:=obj.get(prop_id.scale_x,1.00)) < -1:
        obj[prop_id.scale_x] = -scale_x
        
        if not (flip_x:=obj.get(prop_id.flip_x, False)):
            obj[prop_id.flip_x] = not flip_x
        else:
            obj.pop(prop_id.flip_x, None)
            
    if (scale_y:=obj.get(prop_id.scale_y,1.00)) < -1:
        obj[prop_id.scale_y] = -scale_y
        
        if not (flip_y:=obj.get(prop_id.flip_y, False)):
            obj[prop_id.flip_y] = not flip_y
        else:
            obj.pop(prop_id.flip_y, None)
    
    skew_x = obj.get(prop_id.skew_x,0) % 360
    skew_y = obj.get(prop_id.skew_y,0) % 360
    rotation = obj.get(prop_id.rotation,0) % 360
    
    if skew_x == skew_y:
        rotation += skew_x
        rotation %= 360
        skew_x = skew_y =  0
    
    elif rotation > 0:
        skew_x += rotation
        skew_y += rotation
        skew_x %= 360
        skew_y %= 360
        rotation = 0
    
    if skew_x == skew_y == 0:
        obj.pop(prop_id.skew_x, None)
        obj.pop(prop_id.skew_y, None)
    else:
        obj[prop_id.skew_x] = skew_x
        obj[prop_id.skew_y] = skew_y
        
    if rotation == 0:
        obj.pop(prop_id.rotation, None)
    else:
        obj[prop_id.rotation] = rotation
    

