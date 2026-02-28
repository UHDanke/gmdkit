# Package Imports
from gmdkit.serialization.functions import dataclass_decoder
from gmdkit.serialization.mixins import DataclassDecoderMixin


@dataclass_decoder(slots=True, separator=',', from_array=True)
class MoveButton(DataclassDecoderMixin):
    width: int
    height: int
    scale: float
    opacity: int
    x_pos: float
    y_pos: float
    mode_b: bool
    deadzone: float
    radius: float
    snap: bool
    split: bool


@dataclass_decoder(slots=True, separator=',', from_array=True)
class JumpButton(DataclassDecoderMixin):
    width: int
    height: int
    scale: float
    opacity: int
    x_pos: float
    y_pos: float