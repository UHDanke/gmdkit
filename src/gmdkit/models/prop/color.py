# Package Imports
from gmdkit.models.serialization import DictDecoderMixin, ArrayDecoderMixin, dict_cast
from gmdkit.models.types import DictClass, ListClass
from gmdkit.casting.color import COLOR_DECODERS, COLOR_ENCODERS
from gmdkit.mappings import color_prop
from gmdkit.defaults.color_ids import default_color


class Color(DictDecoderMixin,DictClass):
    
    __slots__ = ()
    
    SEPARATOR = '_'
    DECODER = staticmethod(dict_cast(COLOR_DECODERS,numkey=True))
    ENCODER = staticmethod(dict_cast(COLOR_ENCODERS,default=str))
    
    @property
    def channels(self):
        return self.pluck(color_prop.CHANNEL,color_prop.COPY_ID,ignore_missing=True)
    
    def remap(self, key_value_map):
        if (v:=self.get(color_prop.CHANNEL)) is not None: 
            self[color_prop.CHANNEL] = key_value_map.get(v,v)
        if (v:=self.get(color_prop.COPY_ID)) is not None: 
            self[color_prop.COPY_ID] = key_value_map.get(v,v)

    @classmethod
    def default(cls, color_id:int):        
        return cls(default_color(color_id))

    def set_rgba(self, red:int=None,green:int=None,blue:int=None,alpha:float=None):
        if red is not None: self[color_prop.RED] = min(max(0,red),255)
        if green is not None: self[color_prop.GREEN] = min(max(0,green),255)
        if blue is not None: self[color_prop.BLUE] = min(max(0,blue),255)
        if alpha is not None: self[color_prop.OPACITY] = min(max(0,alpha),255)
        
    def get_rgba(self):
        result = []
        result.append(self.get(color_prop.RED, 255))
        result.append(self.get(color_prop.GREEN, 255))
        result.append(self.get(color_prop.BLUE, 255))
        result.append(self.get(color_prop.OPACITY, 1.00))
        return result
    
    def set_hex(self, hex_string):
        rgb = list(bytes.fromhex(hex_string))
        self.set_rgba(*rgb)


class ColorList(ArrayDecoderMixin,ListClass):

    __slots__ = ()
    
    SEPARATOR = '|'
    DECODER = Color.from_string
    ENCODER = staticmethod(lambda x, **kwargs: x.to_string(**kwargs))
    
    def get_custom(self):
        return self.where(lambda color: 0 < color.get(color_prop.CHANNEL) <= 999)
    
    def get_special(self):
        return self.where(lambda color: color.get(color_prop.CHANNEL) > 999)
    
    def get_channels(self):
        return self.unique_values(lambda color: color.channels)
    
    def get_copies(self):
        return lambda x: x.unique_values(lambda color: color.pluck(color_prop.CHANNEL))
        
    def remap(self, key_value_map):
        self.get_custom().apply(lambda color: color.remap(key_value_map))

    