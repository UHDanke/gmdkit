# Imports
from dataclasses import dataclass
from typing import get_type_hints

# Package Imports
from gmdkit.models.types import ListClass
from gmdkit.models.serialization import ArrayDecoderMixin, DataclassDecoderMixin, dict_cast


class IntList(ArrayDecoderMixin,ListClass):
    
    __slots__ = ()
    
    SEPARATOR = ","
    GROUP_SIZE = 1
    DECODER = int
    
    def __init__(self, *iterable):
        super().__init__(*iterable)
        
    
class IDList(ArrayDecoderMixin,ListClass):
    
    __slots__ = ()
    
    SEPARATOR = "."
    GROUP_SIZE = 1
    DECODER = int
    
    def __init__(self, *iterable):
        super().__init__(*iterable)
    
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
        
        if keys and pair.key not in keys:
            return

        if key_map is not None:
            pair.key = key_map.get(pair.key, pair.key)
            
        if value_map is not None:
            pair.value = value_map.get(pair.value, pair.value)
                
IntPair.DECODER = staticmethod(dict_cast(get_type_hints(IntPair)))


class IntPairList(ArrayDecoderMixin,ListClass):
    
    __slots__ = ()
    
    SEPARATOR = "."
    GROUP_SIZE = 2
    DECODER = staticmethod(lambda array: IntPair.from_args(*array))
    ENCODER = staticmethod(lambda pair, s=SEPARATOR: pair.to_string(separator=s))
    
    def __init__(self, *iterable):
        super().__init__(*iterable)
   
    def keys(self):
        return self.unique_values(lambda x: x.key)
    
    def values(self):
        return self.unique_values(lambda x: x.value)


class RemapList(IntPairList):
    
    __slots__ = ()
    
    def __init__(self, *iterable):
        super().__init__(*iterable)
        
    @classmethod
    def from_dict(cls, data:dict):
        
        result = cls()
        
        for key, value in data.items():
            result.append(Pair(key,value))
        
        return result
    
    def to_dict(self):
        
        result = {}
        
        for pair in self:
            result[pair.key] = pair.value
        
        return result
    
    def clean(self):
        
        new = {p.key: p.value for p in self}
        new.sort(key=lambda p: p.key)
        self[:] = new
        
    