# Package Imports
from gmdkit.models.serialization import DictDecoderMixin, ArrayDecoderMixin, dict_cast
from gmdkit.models.types import DictClass, ListClass
from gmdkit.casting.color import COLOR_DECODERS, COLOR_ENCODERS
from gmdkit.mappings import color_prop, color_id

class Color(DictDecoderMixin,DictClass):
    
    __slots__ = ()
    
    SEPARATOR = '_'
    DECODER = staticmethod(dict_cast(COLOR_DECODERS))
    ENCODER = staticmethod(dict_cast(COLOR_ENCODERS))
    
    @property
    def channels(self):
        return self.pluck(6,9,ignore_missing=True)
    
    def remap(self, key_value_map):
        if (v:=self.get(color_prop.CHANNEL)) is not None: 
            self[color_prop.CHANNEL] = key_value_map.get(v,v)
        if (v:=self.get(color_prop.COPY_ID)) is not None: 
            self[color_prop.COPY_ID] = key_value_map.get(v,v)

    @classmethod
    def default(self, color):
        match color:
            case color_id.BACKGROUND:
                self.set_rgba(40,125,255)
                self[color_prop.DISABLE_OPACITY] = True
            case color_id.GROUND:
                self.set_rgba(0,102,255)
                self[color_prop.DISABLE_OPACITY] = True
            case color_id.LINE:
                self.set_rgba(255,255,255)
                self[color_prop.BLENDING] = True
            case color_id.LINE_3D:
                self.set_rgba(255,255,255)
            case color_id.OBJECT:
                self.set_rgba(255,255,255)
            case color_id.GROUND_2:
                self.set_rgba(0,102,255)
                self[color_prop.DISABLE_OPACITY] = True
            case color_id.MIDDLEGROUND:
                self.set_rgba(40,125,255)
            case color_id.MIDDLEGROUND_2:
                self.set_rgba(40,125,255)                
            case _:
                self.set_rgba(255,255,255)
        
        return self
        
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
        
    def remap(self, key_value_map):
        self.get_custom().apply(lambda color: color.remap(key_value_map))

    