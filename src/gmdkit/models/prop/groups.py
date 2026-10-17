# Package Imports
from gmdkit.models.prop.list import IntList


class IDList(IntList):
    
    SEPARATOR = "."
    
    def remap(self, kv_map:dict[int,int]):
        kv_get = kv_map.get
        self[:] = [kv_get(x,x) for x in self]


class CenterID(int):
    def __repr__(self):
        return f"CenterID({int(self)})"


class ParentIDList(IDList):
    DECODER = staticmethod(lambda i: CenterID(i) if i.startswith("+") else int(i))
    ENCODER = staticmethod(lambda i: ('+' if type(i) is CenterID else '') + str(i))

    def add_center(self, i: int):
        center = CenterID(i)
        for idx, existing in enumerate(self):
            if existing == center:
                self[idx] = center
                return
        self.append(center)