# Imports
from typing import Self

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.utils import enums
from gmdkit.serialization.mixins import DataclassDecoderMixin, ArrayDecoderMixin, DictDecoderMixin
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.serialization.type_cast import to_bool,from_bool,from_float, decode_text, encode_text


KEY_MASK = 0xFFFF
MOD_CTRL = 0x10000
MOD_ALT = 0x20000
MOD_SHIFT = 0x40000
CONTROLLER_MIN = 1001
CONTROLLER_MAX = 1044


class InputKey(int):

    @classmethod
    def modify(cls, key:int, ctrl:bool=False, alt:bool=False, shift:bool=False) -> Self:
        if CONTROLLER_MIN <= (key & KEY_MASK) <= CONTROLLER_MAX:
            return cls(key & KEY_MASK)
        return cls(key | (MOD_CTRL if ctrl else 0) | (MOD_ALT if alt else 0) | (MOD_SHIFT if shift else 0))

    @property
    def key(self) -> int:
        return self & KEY_MASK

    @property
    def ctrl(self) -> bool:
        return bool(self & MOD_CTRL)

    @property
    def alt(self) -> bool:
        return bool(self & MOD_ALT)

    @property
    def shift(self) -> bool:
        return bool(self & MOD_SHIFT)

    @property
    def is_controller(self) -> bool:
        return CONTROLLER_MIN <= self.key <= CONTROLLER_MAX


class InputKeyList(ArrayDecoderMixin, ListClass[InputKey]):

    __slots__ = ()

    SEPARATOR = ","
    DECODER = staticmethod(lambda s: InputKey(int(s)))
    ENCODER = staticmethod(str)


class ControlKeybindDict(DictDecoderMixin, DictClass[int, InputKeyList]):
    SEPARATOR = ";"
    PAIR_SEPARATOR = ","
    SINGLE_SPLIT = True
    SORT_KEYS = True
    DECODER = staticmethod(lambda k, v: (int(k), InputKeyList.from_string(v)))
    ENCODER = staticmethod(lambda k, v: (str(k), v.to_string()))


@dataclass_decoder(slots=True, separator=",", from_array=False, pair_separator="=", single_split=True)
class ControlSlot(DataclassDecoderMixin):
    anchor_x: int = field_decoder(key="ax", default=0)
    anchor_y: int = field_decoder(key="ay", default=0)
    relative_x: bool = field_decoder(key="rx", default=False, decoder=to_bool, encoder=from_bool)
    relative_y: bool = field_decoder(key="ry", default=False, decoder=to_bool, encoder=from_bool)
    offset_x: float = field_decoder(key="ox", default=0.0, encoder=from_float)
    offset_y: float = field_decoder(key="oy", default=0.0, encoder=from_float)
    width: int = field_decoder(key="w", default=280)
    height: int = field_decoder(key="h", default=120)
    scale: float = field_decoder(key="s", default=1.0, encoder=from_float)
    opacity: int = field_decoder(key="o", default=255)
    deadzone: float = field_decoder(key="dz", default=0.0, encoder=from_float)
    radius: float = field_decoder(key="rd", default=10.0, encoder=from_float)
    mode_b: bool = field_decoder(key="mb", default=False, decoder=to_bool, encoder=from_bool)
    snap: bool = field_decoder(key="sr", default=False, decoder=to_bool, encoder=from_bool)
    split: bool = field_decoder(key="ns", default=False, decoder=to_bool, encoder=from_bool)
    one_button: bool = field_decoder(key="ob", default=False, decoder=to_bool, encoder=from_bool)


class ControlSlotList(ArrayDecoderMixin, ListClass[ControlSlot]):

    __slots__ = ()

    SEPARATOR = ";"
    DECODER = ControlSlot.from_string
    ENCODER = ControlSlot.to_string


@dataclass_decoder(slots=True, separator=",", from_array=False, pair_separator="=", single_split=True)
class TouchCanvas(DataclassDecoderMixin):
    width: float = field_decoder(key="cw", default=0.0, encoder=from_float)
    height: float = field_decoder(key="ch", default=0.0, encoder=from_float)


@dataclass_decoder(slots=True, separator=";", from_array=True)
class TouchLayout(DataclassDecoderMixin):
    canvas: TouchCanvas = field_decoder(
        default_factory=TouchCanvas,
        decoder=TouchCanvas.from_string,
        encoder=TouchCanvas.to_string
        )
    slots: ControlSlotList = field_decoder(
        default_factory=ControlSlotList,
        decoder=ControlSlotList.from_string,
        encoder=ControlSlotList.to_string,
        optional=True
        )

TouchLayout.MAX_SPLIT = 1


@dataclass_decoder(slots=True, separator="|", from_array=False, pair_separator=":", single_split=True, auto_key=str)
class LevelControls(DataclassDecoderMixin):
    version: int = 1
    keyboard: ControlKeybindDict = field_decoder(
        default_factory=ControlKeybindDict,
        decoder=ControlKeybindDict.from_string,
        encoder=ControlKeybindDict.to_string
        )
    touch: TouchLayout = field_decoder(
        default_factory=TouchLayout,
        decoder=TouchLayout.from_string,
        encoder=TouchLayout.to_string
        )
    flip_platformer_controls: int = 0
    controller: ControlKeybindDict = field_decoder(
        default_factory=ControlKeybindDict,
        decoder=ControlKeybindDict.from_string,
        encoder=ControlKeybindDict.to_string
        )

    @property
    def classes(self) -> enums.ControlType:
        t = enums.ControlType.NONE
        if self.keyboard:      t |= enums.ControlType.KEYBOARD
        if self.touch.slots:   t |= enums.ControlType.TOUCH
        if self.controller:    t |= enums.ControlType.CONTROLLER
        return t
    
    @classmethod
    def from_base64(cls, string:str, **kwargs) -> Self:
        return cls.from_string(decode_text(string + "=" * (-len(string) % 4)), **kwargs)

    def to_base64(self, **kwargs) -> str:
        return encode_text(self.to_string(**kwargs))