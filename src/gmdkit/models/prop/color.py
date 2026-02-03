# Package Imports
from gmdkit.serialization.type_cast import dict_cast, serialize, to_string
from gmdkit.serialization.mixins import DictDecoderMixin, ArrayDecoderMixin
from gmdkit.serialization.types import DictClass, ListClass
from gmdkit.casting.color import COLOR_DECODERS, COLOR_ENCODERS
from gmdkit.mappings import color_prop
from gmdkit.defaults.color_ids import default_color


class Color(DictDecoderMixin,DictClass):
    
    __slots__ = ()
    
    SEPARATOR = '_'
    DECODER = staticmethod(dict_cast(COLOR_DECODERS,numkey=True))
    ENCODER = staticmethod(dict_cast(COLOR_ENCODERS,default=serialize))
    
    @classmethod
    def default(cls, color_id:int):        
        return cls(default_color(color_id))

    def set_rgba(self, red:int|None=None,green:int|None=None,blue:int|None=None,alpha:float|None=None):
        if red is not None: self[color_prop.RED] = red
        if green is not None: self[color_prop.GREEN] = green
        if blue is not None: self[color_prop.BLUE] = blue
        if alpha is not None: self[color_prop.OPACITY] = alpha
    
    def get_rgba(self):
        r = self.get(color_prop.RED, 255)
        g = self.get(color_prop.GREEN, 255)
        b = self.get(color_prop.BLUE, 255)
        a = self.get(color_prop.OPACITY, 1.00)
        return (r,g,b,a)
    
    def set_hex(self, hex_string):
        hex_string = hex_string.lstrip("#")
        if len(hex_string) != 6:
            raise ValueError("Invalid hex string.")
        
        r = int(hex_string[0:2], 16)
        g = int(hex_string[2:4], 16)
        b = int(hex_string[4:6], 16)
        self.set_rgba(r, g, b)
    
    def get_hex(self):
        r, g, b, _ = self.get_rgba()
        return "#{:02X}{:02X}{:02X}".format(r, g, b)


class ColorList(ArrayDecoderMixin,ListClass):

    __slots__ = ()
    
    SEPARATOR = '|'
    KEEP_SEP = True
    DECODER = Color.from_string
    ENCODER = staticmethod(to_string)
    
    def get_channels(self, condition):
        return self.unique_values(lambda color: color.pluck(color_prop.CHANNEL))
    
    def get_copies(self):
        return lambda x: x.unique_values(lambda color: color.pluck(color_prop.COPY_ID))