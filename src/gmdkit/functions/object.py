# Imports
import math
from typing import Optional

# Package Imports
from gmdkit.models.object import Object
from gmdkit.models import interfaces
from gmdkit.utils import enums


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
    intf = obj.require_interface(interfaces.BaseObject)
    
    if not lock_scale:
        intf.scale_x *= scale_x
        intf.scale_y *= scale_y
    
    if center_x is not None:
        intf.x = center_x + scale_x * (intf.x - center_x)
    
    if center_y is not None:
        intf.x = center_x + scale_x * (intf.x - center_y)


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
    intf = obj.require_interface(interfaces.BaseObject)
    
    if not lock_rotation:
        if intf.skew_x % 360 == intf.skew_y % 360 == 0:
            intf.rotation += angle
        
        else:
            intf.skew_x += angle
            intf.skew_y += angle

    if center_x is not None and center_y is not None:
        th = math.radians(angle)

        dx = intf.x - center_x
        dy = intf.y - center_y

        intf.x = dx * math.cos(th) - dy * math.sin(th)
        intf.y = dx * math.sin(th) + dy * math.cos(th)


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
    intf = obj.require_interface(interfaces.SecretCoin,None)
    if intf:
        intf.obj_id = enums.ObjectID.COLLECTIBLE_USER_COIN
        del intf.coin_id 

