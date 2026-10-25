# Imports
from typing import Optional, Sequence, Self

# Package Imports
from gmdkit.utils.types import ListClass
from gmdkit.serialization.mixins import DataclassDecoderMixin, ArrayDecoderMixin, DelimiterMixin
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.utils.enums import TargetPlayer

@dataclass_decoder(slots=True, separator='a', from_array=True)
class HSV(DataclassDecoderMixin):
    
    hue: float = 0
    saturation: float = 1
    value: float = 1
    saturation_add: bool = False
    value_add: bool = False
    

@dataclass_decoder(slots=True, from_array=False, separator="_", auto_key=str)
class RGB(DataclassDecoderMixin):
    red: int = 0
    green: int = 0
    blue: int = 0
    
    def set_rgb(
            self,
            red:Optional[int]=None,
            green:Optional[int]=None,
            blue:Optional[int]=None
            ):
        if red is not None:
            self.red = red

        if green is not None:
            self.green = green

        if blue is not None:
            self.blue = blue
            
    def get_rgb(self) -> tuple[int,int,int]:
        return tuple(self.red,self.green,self.blue)

    def set_hex(self, hex_string):
        hex_string = hex_string.lstrip("#")
        if len(hex_string) != 6:
            raise ValueError("Invalid hex string.")

        r = int(hex_string[0:2], 16)
        g = int(hex_string[2:4], 16)
        b = int(hex_string[4:6], 16)
        self.set_rgb(r, g, b)

    def get_hex(self) -> tuple[int,int,int]:
        r, g, b, _ = self.get_rgb()
        return "#{:02X}{:02X}{:02X}".format(r, g, b)

DEFAULT_LEVEL_COLORS = {
    1000: (40, 125, 255, False),
    1001: (0, 102, 255, False),
    1002: (255, 255, 255, True),
    1005: (192, 255, 224, True),
    1006: (255, 185, 0, True),
    1009: (0, 102, 255, False),
    1013: (40, 125, 255, False),
    1014: (40, 125, 255, False),
    }

@dataclass_decoder(slots=True, from_array=False, separator="_", auto_key=str)
class Color(RGB):

    player: TargetPlayer = field_decoder(default=TargetPlayer.NONE,decoder=TargetPlayer.from_string,encoder=str)
    blending: bool = field_decoder(default=False,optional=True)
    channel: int = 0
    opacity: float = 0.0
    use_opacity: bool = True
    copy_id: int = field_decoder(default=0,optional=True)
    hsv: HSV = field_decoder(default_factory=HSV,optional=True,decoder=HSV.from_string,encoder=HSV.to_string)
    to_red: int = 0
    to_green: int = 0
    to_blue: int = 0
    time_delta: float = field_decoder(default=0.0,optional=True)
    to_opacity: float = 0.0
    duration: float = field_decoder(default=0.0,optional=True)
    copy_opacity: bool = field_decoder(default=False,optional=True)
    runtime_trigger_id: int = 0
    paused: bool = field_decoder(default=False,optional=True)


    @classmethod
    def default(cls, channel:int) -> Self:
        channel = min(max(int(channel), 0), 1101)
        red, green, blue, blending = DEFAULT_LEVEL_COLORS.get(channel, (255, 255, 255, False))
        return cls(
            red=red, green=green, blue=blue,
            player=TargetPlayer.NONE,
            blending=blending,
            channel=channel,
            opacity=1.0,
            use_opacity=True,
            to_red=255, to_green=255, to_blue=255,
            to_opacity=1.0,
            )

    def is_default(self):
        channel = self.channel

        value = (
            self.red,
            self.green,
            self.blue,
            self.player,
            self.blending,
            self.opacity,
            self.copy_id,
        )

        if  channel <= 999 or channel >=1015:
            if value == (255,255,255,TargetPlayer.NONE,False,1.0,0):
                return True
        elif channel in {1005,1006,1008}:
            return True

    def has_hsv(self) -> bool:
        return not type(self).CONDITION("hsv",v=self.hsv)


class ColorList(DelimiterMixin,ArrayDecoderMixin,ListClass[Color]):

    __slots__ = ()

    SEPARATOR = '|'
    END_DELIMITER = "|"
    DECODER = Color.from_string
    ENCODER = Color.to_string

    def get_channels(self):
        return self.unique_values(lambda color: (color.channel,))

    def get_copies(self):
        return self.unique_values(lambda color: (color.copy_id,))

    def discard_duplicates(self):
        seen = set()
        i = 0

        while i < len(self):
            channel = self[i].channel
            if channel in seen:
                del self[i]
            else:
                seen.add(channel)
                i += 1

    def set_defaults(self, *color_ids:int, override:bool=False):
        existing = self.get_channels()
        ids = set(color_ids)
        if override:
            self[:] = [c for c in self if c.id not in ids]
        else:
            ids -= existing
        for i in ids:
            self.append(Color.default(i))

    def clear_defaults(self):
        self[:] = [i for i in self if not i.is_default()]

    def add_colors(self, colors:Sequence[Color], override:bool=False):
        index = {c.channel: i for i, c in enumerate(self)}

        for color in colors:
            if color.channel in index:
                if override:
                    self[index[color.channel]] = color
            else:
                index[color.channel] = len(self)
                self.append(color)