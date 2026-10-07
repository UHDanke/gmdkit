# Package Imports
from gmdkit.models.object import Object, ObjectList
from gmdkit.functions.object_list import compile_keyframe_groups
from gmdkit.models import interfaces


def compile_keyframe_spawn_ids(obj_list:ObjectList):
    
    def key_func(obj:Object):
        intf = obj.require_interface(interfaces.KeyframeObject,None)
        if intf is None: return
        spawn_id = intf.spawn_id
        return None if spawn_id == 0 else spawn_id
    
    return compile_keyframe_groups(obj_list,key_func)


def compile_spawn_groups(obj_list:ObjectList):
    
    spawn_groups = { 0: ObjectList() }
    
    for obj in obj_list:
        intf = obj.require_interface(interfaces.TriggerObject,None)
        if not intf: continue
        
        if not (groups:=intf.groups):
            for i in set(groups):
                spawn_groups.setdefault(i,ObjectList())
                spawn_groups[i].append(obj)
        else:
            spawn_groups[0].append(obj)
    
    for v in spawn_groups.values():
        v.sort(key=lambda obj: obj.interface.x)
        
    return spawn_groups
