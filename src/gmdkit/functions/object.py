# Imports
import math
from typing import Optional

# Package Imports
from gmdkit.models.object import Object
from gmdkit.mappings import obj_prop, obj_id


def scale_position(
        obj:Object,
        scale_x:float=1.00,
        scale_y:float=1.00,
        center_x:Optional[float]=None, 
        center_y:Optional[float]=None, 
        lock_scale:bool=False
        ):
    """
    Scales and moves an object relative to a position.

    Parameters
    ----------
    obj : Object
        The object to modify.
    scale_x : float, optional
        The X scaling applied, defaults to 1.00.
    scale_y : float, optional
        The Y scaling applied, defaults to 1.00.
    center_x : Optional[float], optional
        The X position of the center reference, movement is not applied on X axis if left as None.
    center_y : Optional[float], optional
        The Y position of the center reference, movement is not applied on X axis if left as None.
    lock_scale : bool, optional
        Only moves the object without scaling if True, defaults to False.

    Returns
    -------
    None.

    """
    
    if not lock_scale:
        obj[obj_prop.SCALE_X] = obj.get(obj_prop.SCALE_X, 1.00) * scale_x
        obj[obj_prop.SCALE_Y] = obj.get(obj_prop.SCALE_Y, 1.00) * scale_y
    
    if center_x is not None and (x:=obj.get(obj_prop.X)) is not None:
        obj[obj_prop.X] = center_x + scale_x * (x - center_x)
     
    if center_y is not None and (y:=obj.get(obj_prop.Y)) is not None:
        obj[obj_prop.Y] = center_y+scale_y * (y - center_y)

def rotate_position(
        obj:Object,
        angle:float=0, 
        center_x:Optional[float]=None, 
        center_y:Optional[float]=None, 
        lock_rotation:bool=False
        ):
    """
    Rotates and moves an object relative to a position.

    Parameters
    ----------
    obj : Object
        The object to modify.
    angle : float, optional
        The angle of the rotation that will be applied, defaults to 0.
    center_x : Optional[float], optional
        The X position of the center reference, movement is not applied on X axis if left as None.
    center_y : Optional[float], optional
        The Y position of the center reference, movement is not applied on X axis if left as None.
    lock_rotation : bool, optional
        Only moves the object without rotation if True, defaults to False.
    Returns
    -------
    None.

    """
    
    if not lock_rotation:
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
                       
def to_user_coins(obj:Object):
    """
    Converts secret coins into user coins.

    Parameters
    ----------
    obj : Object
        The object to modify.

    Returns
    -------
    None.

    """
    
    if obj.get(obj_prop.ID) != obj_id.collectible.SECRET_COIN:
        return
        
    obj[obj_prop.ID] = obj_id.collectible.USER_COIN
    obj.pop(obj_prop.trigger.collectible.coin.COIN_ID, None)


