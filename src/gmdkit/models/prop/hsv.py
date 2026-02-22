# Package Imports
from gmdkit.serialization.functions import dataclass_decoder
from gmdkit.serialization.mixins import DataclassDecoderMixin

@dataclass_decoder(slots=True, separator='a', from_array=True)
class HSV(DataclassDecoderMixin):
    
    hue: float = 0
    saturation: float = 1
    value: float = 1
    saturation_add: bool = False
    value_add: bool = False