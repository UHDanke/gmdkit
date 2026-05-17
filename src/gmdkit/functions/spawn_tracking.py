# Package Imports
from gmdkit.models.object import ObjectList
from gmdkit.mappings import obj_prop
from gmdkit.functions.object_list import compile_keyframe_groups


def compile_keyframe_spawn_ids(obj_list:ObjectList):
    
    def key_func(obj):
        spawn_id = obj.get(obj_prop.trigger.keyframe.SPAWN_ID)
        return None if spawn_id == 0 else spawn_id
    
    return compile_keyframe_groups(obj_list,key_func)


def compile_spawn_groups(obj_list:ObjectList):
    
    spawn_groups = { 0: ObjectList() }
    
    for obj in obj_list:
        
        if not obj.get(obj_prop.trigger.SPAWN_TRIGGER):
            continue
        
        if (groups:=obj.get(obj_prop.GROUPS)) is not None:
            
            for i in set(groups):
                spawn_groups.setdefault(i,ObjectList())
                spawn_groups[i].append(obj)
        else:
            spawn_groups[0].append(obj)
    
    for v in spawn_groups.values():
        v.sort(key=lambda obj: obj.get(obj_prop.X))
        
    return spawn_groups
