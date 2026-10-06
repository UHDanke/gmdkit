# Imports
from typing import Optional

# Package Imports
from gmdkit.mappings import obj_id
from gmdkit.models.level import Level
from gmdkit.models.object import Object, ObjectList
from gmdkit.functions.object_list import boundaries, add_groups, group_objects_x
from gmdkit import remapping
from gmdkit.models import interfaces


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
        intf_it = init_toggle.require_interface(interfaces.ToggleTrigger)
        intf_it.x = 0
        intf_it.y = 15+Y
        intf_it.group_id = g
        obj_list.append(init_toggle)
        init_toggles.append(init_toggle)

        start_toggle = Object.default(obj_id.trigger.TOGGLE)
        intf_st = init_toggle.require_interface(interfaces.ToggleTrigger)
        intf_st.x = min_x
        intf_st.y = 15
        intf_st.group_id = g
        intf_st.activate_group = True
        obj_list.append(start_toggle)

        end_toggle = Object.default(obj_id.trigger.TOGGLE)
        intf_et = init_toggle.require_interface(interfaces.ToggleTrigger)
        intf_et.x = max_x
        intf_et.y = 15
        intf_et.group_id = g
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
        intf_ev = event.require_interface(interfaces.TimerEventTrigger)
        intf_ev.x = x
        intf_ev.y = -15
        intf_ev.item_id = target_id
        intf_ev.target_id = i
        intf_ev.target_time = 1.00
        result.append(event)

        if include_stop:
            stop = Object.default(obj_id.trigger.STOP)
            intf_stp = stop.require_interface(interfaces.StopTrigger)
            intf_stp.x = x + stop_offset
            intf_stp.y = -45
            intf_stp.target_id = i
            result.append(stop)

        add_groups(objs, i)
        add_groups((event,), i)

    return result


def create_start_pos_fix_activator(
        target_id,
        pos_x=-165,
        pos_y=-45
        ) -> ObjectList:
     new = ObjectList()
     group = remapping.AutoID()
     
     advf = Object.default(obj_id.trigger.ADV_FOLLOW)
     intf_advf = advf.require_interface(interfaces.AdvancedFollowTrigger)
     intf_advf.x = pos_x
     intf_advf.y = pos_y
     intf_advf.target_id = group
     intf_advf.player_1 = True
     new.append(advf)

     iedit = Object.default(obj_id.trigger.ITEM_EDIT)
     intf_edit = iedit.require_interface(interfaces.ItemEditTrigger)
     intf_edit.groups.append(group)
     intf_edit.x = pos_x+45
     intf_edit.y = pos_y-60
     intf_edit.target_item_id = target_id
     intf_edit.target_item_type = 2
     intf_edit.set_spawn_trigger()
     new.append(iedit)

     return new

def area_start_pos_fix(
        objects,
        target_id:int,
        include_stop:bool=True,
        stop_offset:float=0,
        forward_limit:float=30
        ) -> tuple[ObjectList]:

    def filter_area(obj:Object):
        intf = obj.require_interface(interfaces.area.AreaTrigger,None)
        if intf and not intf.spawn_trigger:
            return True
        return False

    areas = objects.where(filter_area)

    events = start_pos_fix(
        areas,
        target_id=target_id,
        include_stop=include_stop,
        stop_offset=stop_offset,
        forward_limit=forward_limit
        )
    
    for obj in areas:
        obj: Object
        intf = obj.require_interface(interfaces.area.AreaTrigger)
        intf.clear_transforms()
        intf.set_spawn_trigger(True)
    objects += events

    return areas, events



def boundary_offset(
        *levels:Level,
        vertical_stack:bool=False,
        block_offset:int=30
        ):

    i = None
    x = 0
    y = 0
    for level in levels:

        bounds = boundaries(level.objects)

        if vertical_stack:

            if i == None:
                i = bounds[5]

            else:
                y = i
                i += bounds[5]-bounds[1] + block_offset * 30

        else:
            if i == None:
                i = bounds[4]

            else:
                x = i
                i += bounds[4]-bounds[0] + block_offset * 30
        
        for obj in level.objects:
            obj: Object
            intf = obj.require_interface(interfaces.BaseObject)
            intf.x += x
            intf.y += y
            
        i = i // 30 * 30


def get_useless_triggers():
    pass

def get_triggers_with_invalid_targets():
    pass
