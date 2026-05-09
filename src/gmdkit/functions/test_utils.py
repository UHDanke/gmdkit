# Imports
from typing import Sequence, Optional
import math

# Package Imports
from gmdkit import Object, ObjectList
from gmdkit.mappings import obj_prop


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
    
    X = 0
    Y = 0
    i = 0
    for obj in obj_list:
        obj.update(
            {
                obj_prop.X: X,
                obj_prop.Y: Y,
                }
            )
        i+=1
        if i >= height:
            X += 30
            Y = 0
            i = 0 
        else:
            Y-=30