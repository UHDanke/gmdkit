# Imports
from dataclasses import dataclass
from typing import get_type_hints

# Package Imports
from gmdkit.models.serialization import DataclassDecoderMixin, dict_cast


@dataclass(slots=True)
class HSV(DataclassDecoderMixin):

    SEPARATOR = 'a'
    LIST_FORMAT = True
    
    hue: float = 0
    saturation: float = 1
    value: float = 1
    saturation_add: bool = False
    value_add: bool = False


HSV.DECODER = staticmethod(dict_cast(
    {
     key: (lambda x: bool(int(x))) if func is bool else func
     for key, func in get_type_hints(HSV).items()
     }
    ))