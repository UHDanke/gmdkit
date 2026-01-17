# Imports
from dataclasses import dataclass

# Package Imports
from gmdkit.serialization.mixins import DataclassDecoderMixin


@dataclass(slots=True)
class HSV(DataclassDecoderMixin):

    SEPARATOR = 'a'
    LIST_FORMAT = True
    
    hue: float = 0
    saturation: float = 1
    value: float = 1
    saturation_add: bool = False
    value_add: bool = False