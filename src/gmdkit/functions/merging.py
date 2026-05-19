# Imports 
from typing import Optional

# Package Imports
from gmdkit.mappings import obj_prop, obj_id
from gmdkit.models.level import Level
from gmdkit.models.object import Object, ObjectList
from gmdkit.functions.object import reset_transforms, reset_spawn_touch, offset_position
from gmdkit.functions.object_list import boundaries, add_groups, group_objects_x
from gmdkit import remapping
from gmdkit.mappings.obj_id_set import AREA_TRIGGERS


def add_toggles(
        *objects:ObjectList, 
        enable_pos:Optional[float],
        disable_pos:Optional[float],
        include_stop:bool=True
        ):
    init_toggles = ObjectList()
    Y = 0
    for obj_list in objects:
        min_x, min_y, center_x, center_y, max_x, max_y = boundaries(obj_list)
        g = remapping.AutoID()
        
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



def start_pos_fix(
        obj_list:ObjectList, 
        target_id:int,
        forward_limit:float=0,
        include_stop:bool=True,
        stop_offset:float=0
        ):
    
    result = ObjectList()
    
    obj_groups = group_objects_x(obj_list, forward_limit=forward_limit)

    for x, objs in obj_groups.items():
        i = remapping.AutoID()
        
        event = Object.default(obj_id.trigger.TIME_EVENT)
        event.update({
            obj_prop.X: x,
            obj_prop.Y: -15,
            obj_prop.trigger.time_event.ITEM_ID: target_id,
            obj_prop.trigger.time_event.TARGET_ID: i,
            obj_prop.trigger.time_event.TARGET_TIME: 1.00
            })
        result.append(event)
        
        if include_stop:
            stop = Object.default(obj_id.trigger.STOP)
            stop.update({
                obj_prop.X: x + stop_offset,
                obj_prop.Y: -45,
                obj_prop.trigger.stop.TARGET_ID: i,
                })
            result.append(stop)
        
        add_groups(objs+[event], (i,))
    
    return result


def create_start_pos_fix_activator(
        target_id, 
        pos_x=-15, 
        pos_y=-15
        ) -> ObjectList:
     new = ObjectList()
     
     group_ie = remapping.AutoID()
     group_c1 = remapping.AutoID()
     group_c2 = remapping.AutoID()
     
     coll_1 = Object.default(obj_id.trigger.COLLISION_BLOCK)
     coll_1.setdefault(obj_prop.GROUPS).append(group_c1)
     coll_1.update({
         obj_prop.trigger.collision_block.BLOCK_ID: group_c1,
         obj_prop.trigger.collision_block.DYNAMIC: True,
         obj_prop.X: pos_x+45,
         obj_prop.Y: pos_y,
         })
     new.append(coll_1)
    
     coll_2 = Object.default(obj_id.trigger.COLLISION_BLOCK)
     coll_2.setdefault(obj_prop.GROUPS).append(group_c2)
     coll_2.update({
         obj_prop.trigger.collision_block.BLOCK_ID: group_c2,
         obj_prop.X: pos_x+90,
         obj_prop.Y: pos_y,
         })
     new.append(coll_2)
     
     adv_f = Object.default(obj_id.trigger.ADV_FOLLOW)
     adv_f.update({
         obj_prop.trigger.adv_follow.TARGET_ID: group_c1,
         obj_prop.trigger.adv_follow.FOLLOW_ID: group_c2,
         obj_prop.X: pos_x,
         obj_prop.Y: pos_y,
         })
     new.append(adv_f)
     
     coll_t = Object.default(obj_id.trigger.COLLISION)
     coll_t.update({
         obj_prop.trigger.collision.BLOCK_A: group_c1,
         obj_prop.trigger.collision.BLOCK_B: group_c2,
         obj_prop.trigger.collision.ACTIVATE_GROUP: True,
         obj_prop.trigger.collision.TARGET_ID: group_ie,
         obj_prop.X: pos_x,
         obj_prop.Y: pos_y-60,
         })
     new.append(coll_t)
     
     item_e = Object.default(obj_id.trigger.ITEM_EDIT)
     item_e.setdefault(obj_prop.GROUPS).append(group_ie)
     item_e.update({
         obj_prop.trigger.item_edit.TARGET_ITEM_ID: target_id,
         obj_prop.trigger.item_edit.MOD: 1.0,
         obj_prop.trigger.item_edit.ITEM_TYPE_3: 2,
         obj_prop.trigger.SPAWN_TRIGGER: True,
         obj_prop.X: pos_x+45,
         obj_prop.Y: pos_y-60,
         })
     new.append(item_e)
     
     return new

def area_start_pos_fix(
        objects,
        target_id:int,
        include_stop:bool=True,
        stop_offset:float=0,
        forward_limit:float=30
        ) -> tuple[ObjectList]:
    
    def filter_area(obj):
        return obj.get(obj_prop.ID) in AREA_TRIGGERS and not obj.get(obj_prop.trigger.SPAWN_TRIGGER)
    
    def add_spawn(obj):
        obj[obj_prop.trigger.SPAWN_TRIGGER] = True
    
    areas = objects.where(filter_area)
    
    events = start_pos_fix(
        areas,
        target_id=target_id,
        include_stop=include_stop,
        stop_offset=stop_offset,
        forward_limit=forward_limit
        )
    
    areas.apply(reset_transforms,reset_spawn_touch,add_spawn)
    
    objects += events
    
    return areas, events
    


def boundary_offset(
        *levels:Level,
        vertical_stack:bool=False,
        block_offset:int=30
        ):
    
    i = None
    
    for level in levels:
    
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
   





def get_useless_triggers():
    pass

def get_triggers_with_invalid_targets():
    pass
        