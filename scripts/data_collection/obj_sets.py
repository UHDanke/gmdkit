from gmdkit import ObjectList
from gmdkit.utils.misc import Clipboard
from gmdkit.mappings.obj_id_alias import ALIASES

def to_frozenset(objects:ObjectList):
    ids = frozenset(objects.unique_values(lambda obj: obj.pluck(1)))
    return (
        "frozenset((\n"
        f"{'\n'.join(
            (
                f'    obj_id.{ALIASES[i]},'
                if i in ALIASES
                else f'    {i},'
            )
            for i in ids
        )}\n"
        "))"
    )
        
    


with Clipboard() as cb:
    try:
        objects = ObjectList.from_string(cb.get())
    except Exception as e:
        raise RuntimeError("Could not grab object list from clipboard") from e
    
    print(to_frozenset(objects))
    