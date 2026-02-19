# Imports
from typing import Optional

# Package Imports
from gmdkit.serialization.mixins import DataclassDecoderMixin
from gmdkit.serialization.decorators import dataclass_decoder, field_decoder
from gmdkit.serialization.type_cast import to_string
from gmdkit.models.prop.replay_data.remaps import RemapData


@dataclass_decoder(slots=True, separator='&', list_format=True)
class TimerData(DataclassDecoderMixin):

    item_id: int
    time: float
    active: bool
    time_mod: int
    ignore_time_warp: bool
    target_time: float
    stop_time: bool
    target_id: int
    trigger_id: int
    control_id: int
    paused: bool
    remaps: Optional[RemapData] = field_decoder(decoder=RemapData.from_string,encoder=to_string)