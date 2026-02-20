# Package Imports
from gmdkit.utils.types import ListClass
from gmdkit.serialization.decorators import dataclass_decoder, field_decoder
from gmdkit.serialization.mixins import (
    DelimiterMixin,
    ArrayDecoderMixin,
    DataclassDecoderMixin
    )
from gmdkit.serialization.type_cast import to_string


class RemapChain(DelimiterMixin, ArrayDecoderMixin, ListClass):
    
    SEPARATOR = "_"
    DECODER = int    

@dataclass_decoder(slots=True, separator='-', list_format=True)
class RemapData(DataclassDecoderMixin):
    
    remap_ids: RemapChain = field_decoder(decoder=RemapChain.from_string,encoder=to_string)
    root_id: int
    
    
RemapData.from_string("12_13_-1251")