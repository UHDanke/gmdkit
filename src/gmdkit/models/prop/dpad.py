# Package Imports
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.serialization.mixins import DataclassDecoderMixin, DelimiterMixin
from gmdkit.serialization.type_cast import to_string


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
    

class SingleLayout(DelimiterMixin,MoveButton):
    END_DELIMITER = ";0"
    
@dataclass_decoder(slots=True, separator=';', from_array=True)
class DualLayout(DataclassDecoderMixin):
    move_p1: MoveButton = field_decoder(decoder=MoveButton.from_string,encoder=to_string)
    move_p2: MoveButton = field_decoder(decoder=MoveButton.from_string,encoder=to_string)
    jump_p1: JumpButton = field_decoder(decoder=JumpButton.from_string,encoder=to_string)
    jump_p2: JumpButton = field_decoder(decoder=JumpButton.from_string,encoder=to_string)