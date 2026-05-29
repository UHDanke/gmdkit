# Imports
from typing import Sequence, Optional

# Package Imports
from gmdkit.remapping.types import AutoID
from gmdkit.models.object import Object, ObjectList
from gmdkit.mappings import obj_id, obj_prop
from gmdkit.utils import enums
from gmdkit.models.prop.remaps import RemapList


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
    obj = Object.default(obj_id.trigger.ITEM_EDIT)
    obj.setdefault(obj_prop.GROUPS).append(target_id)
    obj.update({
        obj_prop.trigger.SPAWN_TRIGGER: True,
        obj_prop.trigger.MULTI_TRIGGER: True,
        obj_prop.trigger.item_edit.TARGET_ITEM_ID: counter,
        obj_prop.trigger.item_edit.ITEM_ID_1: item_id,
        obj_prop.trigger.item_edit.ITEM_TYPE_1: enums.ItemType.ITEM,
        obj_prop.Y: Y,
        })
    result.append(obj)
    
    this_group = spawn_id
    next_target = AutoID()
    
    
    if id_mapping:
        # remap to id mappings
        obj = Object.default(obj_id.trigger.SPAWN)
        obj.setdefault(obj_prop.GROUPS).append(target_id)
        obj.update({
            obj_prop.trigger.SPAWN_TRIGGER: True,
            obj_prop.trigger.MULTI_TRIGGER: True,
            obj_prop.trigger.spawn.GROUP_ID: next_target,
            obj_prop.trigger.spawn.REMAPS: RemapList.from_dict(id_mapping),
            obj_prop.Y: Y,
            obj_prop.X: 30
            })
        result.append(obj)
        
        this_group = next_target
        next_target = AutoID()
    
    remap_target = AutoID()
    
    for i in range(bit,-1,-1):
        v = 2 ** i
        
        kv_map = dict(zip(values[:v],values[v:]))
        
        print(v)
        print(kv_map)
        # bit comparer
        obj = Object.default(obj_id.trigger.ITEM_COMPARE)
        obj.setdefault(obj_prop.GROUPS).append(this_group)
        obj.update({
            obj_prop.trigger.SPAWN_TRIGGER: True,
            obj_prop.trigger.MULTI_TRIGGER: True,
            obj_prop.trigger.item_compare.TRUE_ID: remap_target,
            obj_prop.trigger.item_compare.FALSE_ID: next_target,
            obj_prop.trigger.item_compare.ITEM_ID_1: counter,
            obj_prop.trigger.item_compare.ITEM_OP_3: enums.ItemOperation.ADD_GT,
            obj_prop.trigger.item_compare.MOD_2: v,
            obj_prop.Y: Y,
            obj_prop.X: 30*3,
            })
        result.append(obj)        
        
        Y -= 30
        
        # bit shift
        obj = Object.default(obj_id.trigger.ITEM_EDIT)
        obj.setdefault(obj_prop.GROUPS).append(remap_target)
        obj.update({
            obj_prop.trigger.SPAWN_TRIGGER: True,
            obj_prop.trigger.MULTI_TRIGGER: True,
            obj_prop.trigger.item_edit.TARGET_ITEM_ID: counter,
            obj_prop.trigger.item_edit.ITEM_OP_1: enums.ItemOperation.DIVIDE_LE,
            obj_prop.trigger.item_edit.MOD: 2.0,
            obj_prop.Y: Y,
            })
        result.append(obj)
        
        # remapper
        obj = Object.default(obj_id.trigger.SPAWN)
        obj.setdefault(obj_prop.GROUPS).append(remap_target)
        obj.update({
            obj_prop.trigger.SPAWN_TRIGGER: True,
            obj_prop.trigger.MULTI_TRIGGER: True,
            obj_prop.trigger.spawn.GROUP_ID: next_target,
            obj_prop.trigger.spawn.REMAPS: RemapList.from_dict(kv_map),
            obj_prop.Y: Y,
            obj_prop.X: 30
            })
        result.append(obj)
        
        this_group = next_target
        next_target = AutoID()
    
        if i > 0:
            remap_target = AutoID()
    
    Y -= 30
    
    # spawn trigger
    obj = Object.default(obj_id.trigger.SPAWN)
    obj.setdefault(obj_prop.GROUPS).append(this_group)
    obj.update({
        obj_prop.trigger.SPAWN_TRIGGER: True,
        obj_prop.trigger.MULTI_TRIGGER: True,
        obj_prop.trigger.spawn.GROUP_ID: spawn_id,
        obj_prop.trigger.spawn.REMAPS: RemapList.from_dict({target_id: values[0]}),
        obj_prop.Y: Y
        })
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