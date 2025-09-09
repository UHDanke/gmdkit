# Package Imports
from gmdkit.models.serialization import DictDecoderMixin, ArrayDecoderMixin, dict_cast
from gmdkit.models.types import DictClass, ListClass
from gmdkit.casting.color import COLOR_DECODERS, COLOR_ENCODERS
from gmdkit.mappings import color_prop 

class Color(DictDecoderMixin,DictClass):
    
    __slots__ = ()
    
    SEPARATOR = '_'
    DECODER = staticmethod(dict_cast(COLOR_DECODERS))
    ENCODER = staticmethod(dict_cast(COLOR_ENCODERS))
    
    @property
    def channels(self):
        return self.pluck(6,9,ignore_missing=True)
    
    def remap(self, key_value_map):
        if (v:=self.get(6)) is not None: self[6] = key_value_map.get(v,v)
        if (v:=self.get(9)) is not None: self[9] = key_value_map.get(v,v)


class ColorList(ArrayDecoderMixin,ListClass):

    __slots__ = ()
    
    SEPARATOR = '|'
    DECODER = Color.from_string
    ENCODER = staticmethod(lambda x, **kwargs: x.to_string(**kwargs))