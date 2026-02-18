# Package Imports
from gmdkit.serialization.decorators import dataclass_decoder

@dataclass_decoder(slots=True, separator='a', list_format=True)
class HSV:

    SEPARATOR = 'a'
    LIST_FORMAT = True
    
    hue: float = 0
    saturation: float = 1
    value: float = 1
    saturation_add: bool = False
    value_add: bool = False