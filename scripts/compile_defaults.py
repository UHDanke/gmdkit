from gmdkit.models.object import Object, ObjectList
from gmdkit.mappings import obj_id, obj_prop


pool = ObjectList.from_file("data/txt/default.txt")


def clean_obj(obj):
    
    obj.pop(obj_prop.COLOR_1_INDEX,None)
    obj.pop(obj_prop.COLOR_2_INDEX,None)
    
    if obj_prop.X in obj:
        obj[obj_prop.X] = 0
    
    if obj_prop.Y in obj:
        obj[obj_prop.Y] = 0
    
    if obj.get(obj_prop.ID) == obj_id.PARTICLE_OBJECT:
        
        obj[obj_prop.particle.DATA] = "30a-1a1a0.3a30a90a90a29a0a11a0a0a0a0a0a0a0a2a1a0a0a1a0a1a0a1a0a1a0a1a1a0a0a1a0a1a0a1a0a1a0a0a0a0a0a0a0a0a0a0a0a0a2a1a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0"
        
        
pool.apply(clean_obj)


default = dict()

for obj in pool:
    object_id = obj.get(obj_prop.ID)
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
