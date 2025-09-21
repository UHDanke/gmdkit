# Imports
import math
from typing import Any

# Package Imports
from gmdkit.models.object import Object
from gmdkit.mappings import color_id, obj_prop, obj_id
    

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
    if (groups:=obj.get(obj_prop.GROUPS)) is not None:
        
        obj[obj_prop.GROUPS][:] = set(groups)


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
    if obj.get(obj_prop.ID) == obj_id.trigger.SPAWN and (remaps:=obj.get(obj_prop.trigger.spawn.REMAPS)) is not None:
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
    
    if obj.get(obj_prop.ID) in shader_triggers:
        
        if obj_prop.COLOR_1 not in obj:
            
            obj[obj_prop.COLOR_1] = color_id.WHITE



def fix_lighter(obj:Object, replacement:int=color_id.WHITE) -> None:
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
    if obj.get(obj_prop.COLOR_1) == color_id.LIGHTER:
        
        obj[obj_prop.COLOR_1] = replacement
    

def pop_zeros(obj:Object) -> None:
    """
    Removes object properties with value 0.

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
    if obj.get(obj_prop.X) is not None:
        obj[obj_prop.X] += offset_x
        
    if obj.get(obj_prop.Y) is not None:
        obj[obj_prop.Y] += offset_y


def scale_position(
        obj:Object,
        scale_x:float=1.00,scale_y:float=1.00,
        center_x:float=None, center_y:float=None, 
        only_move:bool=False
        ) -> None:
    
    if not only_move:
        obj[obj_prop.SCALE_X] = obj.get(obj_prop.SCALE_X, 1.00) * scale_x
        obj[obj_prop.SCALE_Y] = obj.get(obj_prop.SCALE_Y, 1.00) * scale_y
    
    if center_x is not None and (x:=obj.get(obj_prop.X)) is not None:
        obj[obj_prop.X] = scale_x * (x - center_x)
     
    if center_y is not None and (x:=obj.get(obj_prop.X)) is not None:
        obj[obj_prop.Y] = scale_y * (y - center_y)


def rotate_position(
        obj:Object,
        angle:float=0, 
        center_x:float=None, center_y:float=None, 
        only_move:bool=False
        ):
    
    if not only_move:
        skew_x = obj.get(obj_prop.SKEW_X)
        skew_y = obj.get(obj_prop.SKEW_Y)
        
        if skew_x is None and skew_y is None:
            obj[obj_prop.ROTATION] = obj.get(obj_prop.ROTATION,0) + angle
        
        else:
            obj[obj_prop.SKEW_X] = skew_x or 0 + angle
            obj[obj_prop.SKEW_Y] = skew_y or 0 + angle

    if (
            center_x is not None and center_y is not None 
            and (x:=obj.get(obj_prop.X)) is not None 
            and (y:=obj.get(obj_prop.Y)) is not None
            ):
        th = math.radians(angle)

        dx = x - center_x
        dy = y - center_y

        obj[obj_prop.X] = dx * math.cos(th) - dy * math.sin(th)
        obj[obj_prop.Y] = dx * math.sin(th) + dy * math.cos(th)


def remap_keys(obj:Object, keys:int|str, value_map:dict[Any,Any]):
    
    for key in set(keys) & obj.keys():
    
        obj[key] = value_map.get(obj[key], obj[key])

    
def delete_keys(obj:Object, keys:int|str):
    
    for key in set(keys) & obj.keys():
        
        obj.pop(key)
                  
            
def to_user_coins(obj:Object) -> None:
    
    if obj.get(obj_prop.ID) == obj_id.collectible.SECRET_COIN:
        
        obj[obj_prop.ID] = obj_id.collectible.USER_COIN
        
        obj.pop(obj_prop.trigger.collectible.coin.COIN_ID, None)


def fix_transform(obj) -> None:

    if (scale_x:=obj.get(obj_prop.SCALE_X,1.00)) < -1:
        obj[obj_prop.SCALE_X] = -scale_x
        
        if not (flip_x:=obj.get(obj_prop.FLIP_X, False)):
            obj[obj_prop.FLIP_X] = not flip_x
        else:
            obj.pop(obj_prop.FLIP_X, None)
            
    if (scale_y:=obj.get(obj_prop.SCALE_Y,1.00)) < -1:
        obj[obj_prop.SCALE_Y] = -scale_y
        
        if not (flip_y:=obj.get(obj_prop.FLIP_y, False)):
            obj[obj_prop.FLIP_y] = not flip_y
        else:
            obj.pop(obj_prop.FLIP_Y, None)
    
    skew_x = obj.get(obj_prop.SKEW_X,0) % 360
    skew_y = obj.get(obj_prop.SKEW_Y,0) % 360
    rotation = obj.get(obj_prop.ROTATION,0) % 360
    
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
        obj.pop(obj_prop.SKEW_X, None)
        obj.pop(obj_prop.SKEW_Y, None)
    else:
        obj[obj_prop.SKEW_X] = skew_x
        obj[obj_prop.SKEW_Y] = skew_y
        
    if rotation == 0:
        obj.pop(obj_prop.ROTATION, None)
    else:
        obj[obj_prop.ROTATION] = rotation
    

