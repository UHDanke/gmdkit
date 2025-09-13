from gmdkit.models.object import Object, ObjectList
from gmdkit.mappings import obj_id, prop_id


pool = ObjectList.from_file("../data/txt/default.txt")


def clean_obj(obj):
    
    obj.pop(prop_id.color_1_index,None)
    obj.pop(prop_id.color_2_index,None)
    
    if prop_id.x in obj:
        obj[prop_id.x] = 0
    
    if prop_id.y in obj:
        obj[prop_id.y] = 0
        
    for k,v in obj.items():
        if isinstance(v,(int,bool,float)):
            pass
        else:
            obj[k] = str(v)
    
    if obj.get(prop_id.id) == obj_id.particle_object:
        
        obj[prop_id.particle.data] = "30a-1a1a0.3a30a90a90a29a0a11a0a0a0a0a0a0a0a2a1a0a0a1a0a1a0a1a0a1a0a1a1a0a0a1a0a1a0a1a0a1a0a0a0a0a0a0a0a0a0a0a0a0a2a1a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0"
        
        
pool.apply(clean_obj)


default = dict()

for obj in pool:
    obj_id = obj.get(1)
    default.setdefault(obj_id,dict())
    
    default[obj_id].update(obj)


lines = list()

for key, value in default.items():
    lines.append(f"    {repr(key)}: {repr(value)}")
                 

with open("../src/gmdkit/defaults/objects.py","w") as file:
    
    file.write("Default = {\n")
    
    file.write(',\n'.join(lines))
    
    file.write('\n')
    
    file.write('    }')
