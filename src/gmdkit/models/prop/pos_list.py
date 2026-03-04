# Package Imports
from gmdkit.utils.types import ListClass
from gmdkit.serialization.mixins import ArrayDecoderMixin, DataclassDecoderMixin
from gmdkit.serialization.functions import dataclass_decoder


@dataclass_decoder(slots=True, separator=",", from_array=True)
class Position(DataclassDecoderMixin):
    x: float = 0
    y: float = 0
    

class PositionList(ArrayDecoderMixin,ListClass[Position]):
    
    __slots__ = ()
    
    SEPARATOR = ","
    GROUP_SIZE = 2
    DECODER = Position.from_tokens
    ENCODER = Position.to_tokens