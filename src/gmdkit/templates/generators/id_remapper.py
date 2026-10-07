# Imports
from typing import Sequence, Optional

# Package Imports
from gmdkit.remapping.types import AutoID
from gmdkit.models.object import Object, ObjectList
from gmdkit.utils import enums
from gmdkit.models import interfaces


def generate_id_remapper(
        spawn_id:int,
        item_id:int,
        target_id:int,
        id_range:Sequence[int],
        id_mapping:Optional[dict[int,int]]=None,
        ):
    values = id_range
 
    counter = AutoID()
    n = len(id_range) - 1
    bit = n.bit_length()-1
 
    result = ObjectList()
    Y = 0
 
    # assign item value to counter
    obj = Object.default(enums.ObjectID.TRIGGER_ITEM_EDIT)
    intf = obj.require_interface(interfaces.ItemEditTrigger)
    intf.groups.append(target_id)
    intf.set_spawn_trigger(multi_trigger=True)
    intf.target_item_id = counter
    intf.item_id_1 = item_id
    intf.item_type_1 = enums.ItemType.ITEM
    intf.y = Y
    result.append(obj)
 
    this_group = spawn_id
    next_target = AutoID()
 
 
    if id_mapping:
        # remap to id mappings
        obj = Object.default(enums.ObjectID.TRIGGER_SPAWN)
        intf = obj.require_interface(interfaces.SpawnTrigger)
        intf.groups.append(target_id)
        intf.set_spawn_trigger(multi_trigger=True)
        intf.group_id = next_target
        intf.remaps.update_from_dict(id_mapping)
        intf.x = 30
        intf.y = Y
        result.append(obj)
 
        this_group = next_target
        next_target = AutoID()
 
    remap_target = AutoID()
 
    for i in range(bit,-1,-1):
        v = 2 ** i
 
        kv_map = dict(zip(values[:v],values[v:]))
 
        # bit comparer
        obj = Object.default(enums.ObjectID.TRIGGER_ITEM_COMPARE)
        intf = obj.require_interface(interfaces.ItemCompareTrigger)
        intf.groups.append(this_group)
        intf.set_spawn_trigger(multi_trigger=True)
        intf.true_id = remap_target
        intf.false_id = next_target
        intf.item_id_1 = counter
        intf.comp_op = enums.ItemOperation.ADD_GT
        intf.mod_2 = v
        intf.x = 30*3
        intf.y = Y
        result.append(obj)
 
        Y -= 30
 
        # bit shift
        obj = Object.default(enums.ObjectID.TRIGGER_ITEM_EDIT)
        intf = obj.require_interface(interfaces.ItemEditTrigger)
        intf.groups.append(remap_target)
        intf.set_spawn_trigger(multi_trigger=True)
        intf.target_item_id = counter
        intf.assign_op = enums.ItemOperation.DIVIDE_LE
        intf.mod = 2.0
        intf.y = Y
        result.append(obj)
 
        # remapper
        obj = Object.default(enums.ObjectID.TRIGGER_SPAWN)
        intf = obj.require_interface(interfaces.SpawnTrigger)
        intf.groups.append(remap_target)
        intf.set_spawn_trigger(multi_trigger=True)
        intf.group_id = next_target
        intf.remaps.update_from_dict(kv_map)
        intf.x = 30
        intf.y = Y
        result.append(obj)
 
        this_group = next_target
        next_target = AutoID()
 
        if i > 0:
            remap_target = AutoID()
 
    Y -= 30
 
    # spawn trigger
    obj = Object.default(enums.ObjectID.TRIGGER_SPAWN)
    intf = obj.require_interface(interfaces.SpawnTrigger)
    intf.groups.append(this_group)
    intf.set_spawn_trigger(multi_trigger=True)
    intf.group_id = spawn_id
    intf.remaps.update_from_dict({target_id: values[0]})
    intf.y = Y
    result.append(obj)
 
    return result


if __name__ == "__main__":
    
    id_range = range(-1,-129,-1)
    objs = generate_id_remapper(
        target_id=10,
        item_id=11,
        spawn_id=12,
        id_range=id_range,
        id_mapping=dict(zip(id_range,range(1000,1128)))
        )
    from gmdkit import remapping
    remaps = remapping.resolve_auto_ids(
        objs,
        rules=remapping.rules.REMAP_ID_HANDLER,
        groups=(remapping.rules.REMAP_IDS,)
        )
    string = objs.to_string()