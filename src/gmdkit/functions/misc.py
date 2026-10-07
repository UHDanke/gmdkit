# Imports
from typing import Sequence, Optional
import math

# Package Imports
from gmdkit import Object, ObjectList
from gmdkit.models import interfaces


def objs_from_key(object_ids:Sequence):
    
    obj_list = ObjectList()
    
    for i in object_ids:
        obj_list.append(Object.default(i))
    
    return obj_list

def brickify(obj_list:ObjectList, height:Optional[int]=None):
    """
    Repositions all objects in the list into a compact brick.

    Parameters
    ----------
    obj_list : ObjectList
        The objects to modify.
    height : Optional[int], optional
        The height of the brick. Determined automatically if None.

    Returns
    -------
    None.

    """
    if height is None:
        height = math.ceil(math.sqrt(len(obj_list)))
    
    X = Y = i = 0
    for obj in obj_list:
        intf = obj.require_interface(interfaces.BaseObject)
        intf.x = X
        intf.y = Y
        
        i += 1
        if i >= height:
            X += 30
            Y = i = 0
        else:
            Y-=30