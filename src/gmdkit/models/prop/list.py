# Package Imports
from gmdkit.utils.types import ListClass
from gmdkit.serialization.mixins import ArrayDecoderMixin, DataclassDecoderMixin
from gmdkit.serialization.functions import dataclass_decoder
from gmdkit.utils.enums import GameEvents


class IntList(ArrayDecoderMixin,ListClass[int]):
    
    __slots__ = ()
    
    SEPARATOR = ","
    GROUP_SIZE = 1
    DECODER = int
    ENCODER = str


@dataclass_decoder(slots=True, separator="~", from_array=True)
class IntPair(DataclassDecoderMixin):
    key: int = 0
    value: int = 0
    

class IntPairList(ArrayDecoderMixin,ListClass[IntPair]):
    
    __slots__ = ()
    
    SEPARATOR = "."
    GROUP_SIZE = 2
    DECODER = IntPair.from_tokens
    ENCODER = IntPair.to_tokens
       
    def keys(self):
        return self.unique_values(lambda x: [x.key])
    
    def values(self):
        return self.unique_values(lambda x: [x.value])
    
    def remap_keys(self, dictionary:dict[int,int]):
        if dictionary:
            for pair in self:
                k = pair.key
                pair.key = dictionary.get(k, k)

    
class IDList(IntList):
    
    __slots__ = ()
    
    SEPARATOR = "."
    
    def remap(self, key_value_map:dict[int,int]):
        kv_get = key_value_map.get
        self[:] = [kv_get(x,x) for x in self]


class EventList(IntList[GameEvents]):
    
    __slots__ = ()
    
    SEPARATOR = "."
    
    DECODER = GameEvents.from_string

                    
class RemapList(IntPairList):
    
    __slots__ = ()
    
    @classmethod
    def from_dict(cls, data:dict[int,int]):
        
        result = cls()
        
        for key, value in data.items():
            result.append(IntPair(key,value))
        
        return result
    
    
    def to_dict(self) -> dict[int,int]:
        
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
    
    def remap_vals(self, dictionary:dict):
        if dictionary:
            for pair in self:
                v = pair.value
                pair.value = dictionary.get(v, v)