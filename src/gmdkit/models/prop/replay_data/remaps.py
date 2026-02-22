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
from gmdkit.serialization.type_cast import to_string


class RemapChain(DelimiterMixin, ArrayDecoderMixin, ListClass):
    
    SEPARATOR = "_"
    DECODER = int
    
    def apply_remaps(self, groups:Sequence[int], remaps:dict[int,dict[int,int]]):
        def apply(values, remap_id):
            remap = remaps[remap_id]
            return [remap.get(v, v) for v in values]
        return reduce(apply, self, groups)
                
        
        

@dataclass_decoder(slots=True, separator='-', from_array=True)
class RemapData(DataclassDecoderMixin):
    
    remap_ids: RemapChain = field_decoder(decoder=RemapChain.from_string,encoder=to_string)
    root_id: int