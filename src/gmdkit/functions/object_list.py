# Imports
from typing import Any, Literal
from collections.abc import Callable
from statistics import mean, median

# Package Imports
from gmdkit.mappings import obj_prop, obj_id
from gmdkit.models.object import ObjectList, Object


def clean_gid_parents(obj_list:ObjectList) -> None:
    """
    Removes invisible group ID parents and removes any duplicate references found.

    Parameters
    ----------
    obj_list : ObjectList
        A list of objects to modify.

    Returns
    -------
    None

    """
    seen = set()
    
    for obj in obj_list:
        
        if (parents:=obj.get(obj_prop.PARENT_GROUPS)) is not None:
            
            new = set(parents).intersection(obj.get(obj_prop.GROUPS,[]))
            
            new.difference_update(seen)
            
            seen.update(new)
    
            obj[obj_prop.PARENT_GROUPS][:] = new
                
    
def compile_groups(obj_list:ObjectList) -> dict[int|None,ObjectList]:
    """
    Compiles objects by their group IDs.

    Parameters
    ----------
    obj_list : ObjectList
        A list of objects to compile.

    Returns
    -------
    groups : dict[int, ObjectList]
        A dictionary mapping all objects contained in a group to a group ID.
    """
    groups = {}
    
    groups.setdefault(None, ObjectList())
    
    for obj in obj_list:
        
        gids = obj.get(obj_prop.GROUPS,[])
        
        if gids:
            for gid in gids:
                groups.setdefault(gid,ObjectList())
                groups[gid].append(obj)
        
        else:              
            groups[None].append(obj)
    
    return groups


def compile_parents(obj_list:ObjectList) -> tuple[dict[int|None, ObjectList],dict[int,Object],dict[int,Object],dict[int,Object]]:
    """
    Compiles objects by their groups, group id parents and their group and area parents.

    Parameters
    ----------
    obj_list : ObjectList
        A list of objects to compile.

    Returns
    -------
    groups : dict[int, ObjectList]
        A dictionary mapping all objects contained in a group to a group ID.
        
    group_id_parents: dict[int,Object]
        A dictionary mapping the group ID parent object to a group ID.
        Has priority over other area / group parents if marked as area / group parent.
        
    group_parents: dict[int,Object]
        A dictionary mapping the group parent object to a group ID.
        If multiple exist, the one with smallest x then y position is returned, respecting game mechanics.
        Skipped if no group id parent exists.
        If no group parent exists, the area parent is also the group parent.
        
    area_parents: dict[int,Object]
        A dictionary mapping the area parent object to a group ID.
        If multiple exist, the one with smallest x then y position is returned, respecting game mechanics.
        Skipped if no group id parent exists.
        If no area parent exists, the group parent is also the area parent.
    """
    groups = compile_groups(obj_list=obj_list)
    gid_parents = {}
    group_parents = {}
    area_parents = {}
    
    for obj in obj_list:
        
        if (parents:=obj.get(obj_prop.PARENT_GROUPS)):
        
            for parent in parents:
            
                gid_parents.setdefault(parent, obj)
                
        
    for gid, parent in gid_parents.items():
        
        if parent.get(obj_prop.GROUP_PARENT):
            group_parents[gid] = parent
        
        if parent.get(obj_prop.AREA_PARENT):
            area_parents[gid] = parent
    
    
    priority = lambda obj: (obj.get(obj_prop.X,0),obj.get(obj_prop.Y,0))
    
    for gid, group in groups.items():
        
        if not gid_parents.get(gid):
            continue
        
        gp = group_parents.get(gid)
        ap = area_parents.get(gid)
        
        if gp is None:
            gp = group.where(lambda obj: obj.get(obj_prop.GROUP_PARENT) is not None)
            
            if gp: group_parents[gid] = min(gp, key=priority)
        
        if ap is None:
            ap = group.where(lambda obj: obj.get(obj_prop.AREA_PARENT) is not None)
            
            if ap: area_parents[gid] = min(ap, key=priority)
        
        if gp is None and ap is not None:
            group_parents[gid] = ap
        
        elif ap is None and gp is not None:
            area_parents[gid] = gp
            
    
    return groups, gid_parents, group_parents, area_parents
        
        
def compile_chunks(obj_list:ObjectList, chunk_size:float=100, origin:tuple[float,float]=(0,0), function:Callable=ObjectList) -> dict[tuple[int,int],Any]:
    """
    Compiles objects into their containing chunk.
    Defaults to the chunks the game uses for loading objects.

    Parameters
    ----------
    obj_list : ObjectList
        DESCRIPTION.
        
    chunk_size : float, optional
        The width and height of a chunk. Defaults to 100.
        
    origin : tuple[float,float], optional
        The origin coordinates of the chunk grid. Defaults to (0,0).
        
    function : Callable, optional
        A function to apply on each object list after compiling. Defaults to ObjectList.

    Returns
    -------
    chunks : dict[tuple[int,int],Any]
        A dictionary mapping chunk coordinates to the compiled values.

    """
    ox = origin[0]
    oy = origin[1]
    
    result = dict()
    
    for obj in obj_list:
        x = int(((obj.get(obj_prop.X,ox))-ox)/chunk_size)
        y = int((obj.get(obj_prop.Y,oy)-oy)/chunk_size)
        
        chunk = result.setdefault((x,y),[])
        chunk.append(obj)
            
    return {k:function(v) for k, v in result.items()}


def compile_keyframe_ids(obj_list:ObjectList) -> dict[int,ObjectList]:
    """
    Compiles keyframe objects by their keyframe ID.

    Parameters
    ----------
    obj_list : ObjectList
        The object list to compile.

    Returns
    -------
    keyframe_ids : dict[int,ObjectList]
        A dictionary mapping keyframe IDs to keyframe objects.
    """
    result = dict()
    
    for obj in obj_list:
        
        if obj_id.trigger.KEYFRAME != obj.get(obj_prop.ID):
            continue
        
        if (key_id:=obj.get(obj_prop.trigger.keyframe.KEY_ID, 0)) is not None:
            
            pool = result.setdefault(key_id,ObjectList())
            
            pool.append(obj)
            
    for value in result.values():
        
        value.sort(key=lambda obj: obj.get(obj_prop.trigger.keyframe.INDEX,0))
        
    return result


def compile_keyframe_groups(obj_list:ObjectList) -> dict[int|None,list[int]]:
    """
    Compiles keyframe IDs by group IDs that reference them.

    Parameters
    ----------
    obj_list : ObjectList
        The object list to compile.

    Returns
    -------
    keyframe_groups : dict[int,list[int]]
        A dictionary mapping group IDs to a list of keyframe IDs.

    """
    result = dict()
    
    no_group = set()
    
    for obj in obj_list:
        
        if obj_id.trigger.KEYFRAME != obj.get(obj_prop.ID):
            continue
        
        if (key_id:=obj.get(obj_prop.trigger.keyframe.KEY_ID, 0)) is not None:
            
            groups = obj.get(obj_prop.GROUPS)
            
            if groups:
                no_group.pop(key_id)
                
                for group in groups:
                    key_list = result.setdefault(group,set())
                    key_list.add(key_id)
            else:
                no_group.add(key_id)
    
    if no_group:
        result[None] = no_group
    
    for key, value in result.items():
        
        result[key] = list(result[key]).sort()
        
    return result


def compile_links(obj_list:ObjectList) -> tuple[dict[int, ObjectList],dict[int,Object],dict[int,Object]]:
    """
    Compiles objects by their linked group ID and their group and area parents.

    Parameters
    ----------
    obj_list : ObjectList
        A list of objects to compile.

    Returns
    -------
    links : dict[int, ObjectList]
        A dictionary mapping all objects contained in a linked group to a link ID.

    group_parents: dict[int,Object]
        A dictionary mapping the linked group parent object to a link ID.
        If multiple exist, the one with smallest x then y position is returned, respecting game mechanics.
        If no group parent exists, the area parent is also the group parent.
        
    area_parents: dict[int,Object]
        A dictionary mapping the linked area parent object to a link ID.
        If multiple exist, the one with smallest x then y position is returned, respecting game mechanics.
        If no area parent exists, the group parent is also the area parent.
    """
    links = {}
    group_parents = {}
    area_parents = {}
    
    for obj in obj_list:
        
        if (link_id:=obj.get(obj_prop.LINKED_GROUP)):
        
            link = links.setdefault(link_id,ObjectList())
            link.append(obj)
    
    
    priority = lambda obj: (obj.get(obj_prop.X,0),obj.get(obj_prop.Y,0))
    
    for link_id, link in links.items():
        
        if link_id is None: continue
        
        gp = link.where(lambda obj: obj.get(obj_prop.GROUP_PARENT) is not None)
            
        if gp: group_parents[link_id] = min(gp, key=priority)
        
        ap = link.where(lambda obj: obj.get(obj_prop.AREA_PARENT) is not None)
            
        if ap: area_parents[link_id] = min(ap, key=priority)
            
    return links, group_parents, area_parents


def compile_spawn_groups(obj_list:ObjectList) -> dict[int|None,ObjectList]:
    """
    Compiles spawn triggers by their group IDs.

    Parameters
    ----------
    obj_list : ObjectList
        A list of objects to compile.

    Returns
    -------
    spawn_groups : dict[int|None,ObjectList]
        A dictionary mapping all spawn trigger objects to a group ID.

    """
    spawn_triggers = obj_list.where(lambda obj: obj.get(obj_prop.trigger.SPAWN_TRIGGER,False))
    
    spawn_groups = compile_groups(obj_list=spawn_triggers)
    
    for gid, group in spawn_groups.items():

        group.sort(key=lambda obj: obj.get(obj_prop.X,0))
    
    return spawn_groups


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
        
      
def boundaries(
        obj_list:ObjectList, 
        center_type:Literal["midpoint","mean","median"]="mean"
        ) -> tuple[float|None,float|None,float|None,float|None,float|None,float|None]:
    """
    Compiles the boundaries of a group of objects.
    Only the center position is considered, the object's texture is ignored.

    Parameters
    ----------
    obj_list : ObjectList
        The objects to compile the coordinates of.
        
    center_type : Literal["midpoint","mean","median"], optional
        The method by which to calculate the center of the object group:
        - "midpoint": geometric midpoint between the min and max coordinates.
        - "mean": arithmetic average of all object coordinates.
        - "median": median of all object coordinates.
        
        Defaults to "mean".

    Returns
    -------
    min_x : float
        Minimum X coordinate.
    
    min_y : float
        Minimum Y coordinate.
        
    center_x : float
        Center X coordinate.
        
    center_y : float
        Center Y coordinate.
     
    max_x : float
        Maximum X coordinate.
        
    max_y : float
        Maximum Y coordinate.
    """
    x = []
    y = []
    
    for obj in obj_list:
        if (pos_x:=obj.get(obj_prop.X)) is not None:
            x.append(pos_x)
        if (pos_y:=obj.get(obj_prop.Y)) is not None:
            y.append(pos_y)
    
    if x:
        min_x = min(x)
        max_x = max(x)
        
        match center_type:
            case "midpoint":
                center_x = (max_x + min_x) / 2
            case "mean":
                center_x = mean(x)
            case "median":
                center_x = median(x)
    else:   
        min_x = center_x = max_x = None
    
    if y:
        min_y = min(y)
        max_y = max(y)
        
        match center_type:
            case "midpoint":
                center_y = (max_y + min_y) / 2
            case "mean":
                center_y = mean(y)
            case "median":
                center_y = median(y)
    else:
        min_y = center_y = max_y = None
        
    return min_x, min_y, center_x, center_y, max_x, max_y


def warp_objects(
        obj_list:ObjectList,
        only_move:bool=False,
        rotation:float=None,
        skew_:float=None,
        scale_x:float=None,
        scale_y:float=None,
        center_x:float=None,
        center_y:float=None,
        center_rotation:float=None
        ) -> None:
    
    if center_rotation is not None:
        rotation = (rotation or 0) - center_rotation
        
    r = math.radians(rotation or 0)
    cos_r = math.cos(r)
    sin_r = math.sin(r)
    tx = math.tan(math.radians(skew_x or 0))
    ty = math.tan(math.radians(skew_y or 0))
    
    m00 = cos_r
    m01 = -sin_r + tx
    m10 = sin_r + ty
    m11 = cos_r
    
    for obj in obj_list:
        
        if not only_move:
            
            obj_scale_x = obj.get(obj_prop.SCALE_X, 1.00)
            obj_scale_y = obj.get(obj_prop.SCALE_Y, 1.00)
            obj_skew_x = obj.get(obj_prop.SKEW_X, 0)
            obj_skew_y = obj.get(obj_prop.SKEW_Y, 0)
            
            if (obj_rot:=obj.get(obj_prop.ROTATION)) is not None:
                obj_skew_x += obj_rot
                obj_skew_y += obj_rot
            
            obj_tx = math.radians(obj_skew_x)
            obj_ty = math.radians(obj_skew_y)
            
            vx = obj_scale_x * math.cos(obj_tx)
            vy = obj_scale_x * math.sin(obj_tx)
            wx = obj_scale_y * math.cos(obj_ty)
            wy = obj_scale_y * math.sin(obj_ty)
            
            vx, vy = vx * cos_r - vy * sin_r,  vx * sin_r + vy * cos_r
            wx, wy = wx * cos_r - wy * sin_r, wx * sin_r + wy * cos_r
            
            wx += t_x * vx
            wy += t_x * vy
            vx += t_y * wx
            vy += t_y * wy
        
            obj_scale_x = math.hypot(vx, vy)
            obj_scale_y = math.hypot(wx, wy)
            obj_skew_x = math.degrees(math.atan2(vy, vx))
            obj_skew_y = math.degrees(math.atan2(wy, wx))
        
            if obj_scale_x == 1:
                obj.pop(obj_prop.SCALE_X,None)
            else:
                obj[obj_prop.SCALE_X] = obj_scale_x
            
            if obj_scale_y == 1:
                obj.pop(obj_prop.SCALE_Y,None)
            else:
                obj[obj_prop.SCALE_Y] = obj_scale_y
        
            if obj_skew_x == obj_skew_y:
                obj.pop(obj_prop.SKEW_X, None)
                obj.pop(obj_prop.SKEW_Y, None)
                obj[obj_prop.ROTATION] = obj_skew_x
            
            else:
                obj[obj_prop.SKEW_X] = obj_skew_x
                obj[obj_prop.SKEW_Y] = obj_scale_y
        
        if (x:=obj.get(obj_prop.X)) is not None:
            dx = x - center_x
            obj[obj_prop.X] = m00 * dx + m01 * dy + center_x
                
        if (y:=obj.get(obj_prop.Y)) is not None:
            dy = y - center_y
            obj[obj_prop.Y] = m10 * dx + m11 * dy + center_y
    
    
def align_objects(
        obj_list:ObjectList,
        keep_alignment:bool=False,
        ignore_links:bool=False,
        center_gparent:bool=False,
        x_axis:bool=True,
        y_axis:bool=True
        ) -> None:
    """
    Aligns objects within a group at equal intervals, similar to the Align X / Align Y editor functions.
    Linked objects are aligned as one group, centered on their mean center.
    
    Parameters
    ----------
    obj_list : ObjectList
        The objects to align.
        
    keep_alignment : bool, optional
        Makes objects that share the same position aligned together instead of individually. Defaults to False.
    
    ignore_links: bool, optional
        Whether linked groups are ignored. Defaults to False.
        
    center_gparent : bool, optional
        Use the linked group's group parent instead of its mean center. Defaults to False.
    
    x_axis : bool, optional
        Whether objects are aligned on the x axis. Defaults to True.
    
    y_axis : bool, optional
        Whether objects are aligned on the y axis. Defaults to True.

    Returns
    -------
    None

    """
    if not x_axis or y_axis:
        return
        
    item_list = []
    
    if ignore_links:
        
        for obj in obj_list:
            data = ObjectList([obj])
            x = obj.get(obj_prop.X,0)
            y = obj.get(obj_prop.Y,0)
            item_list.append({'data':data,'x':x,'y':y})
            
    else:
        
        links, group_parents, _ = compile_links(obj_list)
        
        for link_id, link in links.items():
            
            if link_id is None:
                for obj in link:
                    data = ObjectList([obj])
                    x = obj.get(obj_prop.X,0)
                    y = obj.get(obj_prop.Y,0)
                    item_list.append({'data':data,'x':x,'y':y})
            
            else:
                data = link
                
                if center_gparent == True and link_id in group_parents:
                    obj = group_parents[link_id]
                    x = obj.get(obj_prop.X,0)
                    y = obj.get(obj_prop.Y,0)
                
                else:
                    x = mean([obj.get(obj_prop.X,0) for obj in link])
                    y = mean([obj.get(obj_prop.Y,0) for obj in link])
                
                item_list.append({'data':data,'x':x,'y':y})
            
    def per_axis(ax, pid):
        if keep_alignment:
            d = {}
            
            for item in item_list:
                data = d.setdefault(item[ax],[])
                data.extend(item['data'])
                
            l = [{'data':v,ax:k} for k, v in x_dict.items()]
        
        else:
            l = item_list
            
        first = min(l, key=lambda i: i.get(ax,0))
        last = max(l, key=lambda i: i.get(ax,0))
        interval = (last-first) / len(l)
        
        for i, item in enumerate(l):
            offset = first + i*interval - l.get(ax,0)
            
            for obj in item['data']:
                if (val := obj.get(pid)): obj[pid] = val + offset
                
    if x_axis: per_axis('x', obj_prop.X)
    
    if y_axis: per_axis('y', obj_prop.Y)


            
            
            
        
    
