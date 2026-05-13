# Imports
from typing import Sequence
from functools import reduce

# Package Imports
from gmdkit.utils.types import ListClass
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.serialization.mixins import (
    DelimiterMixin,
    ArrayDecoderMixin,
    DataclassDecoderMixin
    )
from gmdkit.models.prop.list import IntPair, IntPairList


class RemapChain(DelimiterMixin, ArrayDecoderMixin, ListClass[int]):
    
    SEPARATOR = "_"
    END_DELIMITER = "_"
    DECODER = int
    ENCODER = str
    
    def apply_remaps(self, groups:Sequence[int], remaps:dict[int,dict[int,int]]):
        def apply(values, remap_id):
            remap = remaps[remap_id]
            return [remap.get(v, v) for v in values]
        return reduce(apply, self, groups)


@dataclass_decoder(slots=True, separator='-', from_array=True)
class RemapData(DataclassDecoderMixin):
    
    remap_ids: RemapChain = field_decoder(decoder=RemapChain.from_string,encoder=RemapChain.to_string)
    root_id: int
        
    
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