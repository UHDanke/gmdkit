# Imports
from dataclasses import dataclass

# Package Imports
from gmdkit.serialization.types import ListClass
from gmdkit.serialization.mixins import ArrayDecoderMixin, DataclassDecoderMixin


class IntList(ArrayDecoderMixin,ListClass):
    
    __slots__ = ()
    
    SEPARATOR = ","
    GROUP_SIZE = 1
    DECODER = int
        
    
class IDList(IntList):
    
    __slots__ = ()
    
    SEPARATOR = "."
    
    def remap(self, key_value_map:dict=None):
        
        if key_value_map is None: return
        
        new = []
        
        for x in self:
            new.append(key_value_map.get(x,x))
        
        self[:] = new


@dataclass(slots=True)
class IntPair(DataclassDecoderMixin):
    
    SEPARATOR = '.'
    LIST_FORMAT = True

    key: int = 0
    value: int = 0
    
    def remap(self, *keys:str, value_map:dict=None, key_map:dict=None):
        
        if keys and self.key not in keys:
            return

        if key_map is not None:
            self.key = key_map.get(self.key, self.key)
            
        if value_map is not None:
            self.value = value_map.get(self.value, self.value)


class IntPairList(ArrayDecoderMixin,ListClass):
    
    __slots__ = ()
    
    SEPARATOR = "."
    GROUP_SIZE = 2
    DECODER = staticmethod(lambda array: IntPair.from_args(*array))
    ENCODER = staticmethod(lambda pair, s=SEPARATOR: pair.to_string(separator=s))
    
    def __init__(self, **kwargs):
        items = [IntPair(k,v) for k,v in kwargs.items()]
        super().__init__(items)
   
    def keys(self):
        return self.unique_values(lambda x: [x.key])
    
    def values(self):
        return self.unique_values(lambda x: [x.value])


class RemapList(IntPairList):
    
    __slots__ = ()
    
    @classmethod
    def from_dict(cls, data:dict):
        
        result = cls()
        
        for key, value in data.items():
            result.append(IntPair(key,value))
        
        return result
    
    
    def to_dict(self):
        
        result = {}
        
        for p in self:
            result[p.key] = max(result.get(p.key, p.value), p.value)
        
        return result
    
    
    def clean(self):
        
        ref = {}
        for p in self:
            ref[p.key] = max(ref.get(p.key, p.value), p.value)
    
        self[:] = [p for p in self if p.value == ref[p.key]]
        self.sort(key=lambda p: (p.key, p.value))
        
    