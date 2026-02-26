# Imports
from typing import Optional

# Package Imports
from gmdkit.utils.types import ListClass
from gmdkit.serialization.type_cast import to_string
from gmdkit.serialization.mixins import DataclassDecoderMixin, ArrayDecoderMixin, DelimiterMixin
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.defaults.color_ids import default_color
from gmdkit.utils.enums import SelectPlayer
from gmdkit.models.prop.hsv import HSV


@dataclass_decoder(slots=True, from_array=False, separator="_", auto_key=str)
class Color(DataclassDecoderMixin):
    
    red: int = 0
    green: int = 0
    blue: int = 0
    player: SelectPlayer = field_decoder(default=SelectPlayer(-1),decoder=SelectPlayer.from_string,encoder=str)
    blending: bool = field_decoder(default=False,optional=True)
    channel: int = 0
    opacity: float = 0.0
    disable_opacity: bool = field_decoder(default=False,optional=True)
    copy_id: int = field_decoder(default=0,optional=True)
    hsv: HSV = field_decoder(default_factory=HSV,optional=True,decoder=HSV.from_string,encoder=to_string)
    to_red: int = 0
    to_green: int = 0
    to_blue: int = 0
    time_delta: float = 0.0
    to_opacity: float = 0.0
    duration: float = field_decoder(default=False,optional=True)
    copy_opacity: bool = field_decoder(default=False,optional=True)
    disable_legacy_hsv: bool = False

    
    @classmethod
    def default(cls, color_id:int):        
        return cls(default_color(color_id))

    def set_rgba(
            self, 
            red:Optional[int]=None,
            green:Optional[int]=None,
            blue:Optional[int]=None,
            alpha:Optional[float]=None
            ):
        if red is not None: 
            self.red = red
            
        if green is not None: 
            self.green = green
        
        if blue is not None: 
            self.blue = blue
        
        if alpha is not None: 
            self.opacity = alpha
    
    def get_rgba(self):
        r = self.red
        g = self.green
        b = self.blue
        a = self.opacity
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


class ColorList(DelimiterMixin,ArrayDecoderMixin,ListClass):

    __slots__ = ()
    
    SEPARATOR = '|'
    END_DELIMITER = "|"
    DECODER = Color.from_string
    ENCODER = staticmethod(to_string)
    
    def get_channels(self, condition):
        return self.unique_values(lambda color: (color.channel,))
    
    def get_copies(self):
        return self.unique_values(lambda color: (color.copy_id,))