from gmdkit import Object, ObjectList
from gmdkit.models import interfaces

pool = ObjectList.from_file("data/txt/default.txt")


def clean_obj(obj:Object):
    intf = obj.require_interface(interfaces.BaseObject)
    del intf.color_1_index
    del intf.color_2_index
    intf.x = 0
    intf.y = 0
    
    intf = obj.require_interface(interfaces.ParticleObject,None)
    if intf:
        intf.data = "30a-1a1a0.3a30a90a90a29a0a11a0a0a0a0a0a0a0a2a1a0a0a1a0a1a0a1a0a1a0a1a1a0a0a1a0a1a0a1a0a1a0a0a0a0a0a0a0a0a0a0a0a0a2a1a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0"
        
        
pool.apply(clean_obj)


default = dict()

for obj in pool:
    intf = obj.require_interface(interfaces.BaseObject)
    object_id = intf.obj_id
    default.setdefault(object_id, dict())
    default[object_id].update(obj)


lines = list()

for key, value in default.items():
    lines.append(f"    {repr(key)}: {repr(value)}")
                 

with open("../src/gmdkit/defaults/objects.py","w") as file:
    
    file.write("Default = {\n")
    
    file.write(',\n'.join(lines))
    
    file.write('\n')
    
    file.write('    }')
