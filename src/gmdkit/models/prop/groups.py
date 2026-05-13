# Package Imports
from gmdkit.models.prop.list import IntList

class IDList(IntList):
    
    __slots__ = ()
    
    SEPARATOR = "."
    
    def remap(self, kv_map:dict[int,int]):
        kv_get = kv_map.get
        self[:] = [kv_get(x,x) for x in self]

