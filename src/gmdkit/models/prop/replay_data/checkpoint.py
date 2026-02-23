# Imports
from typing import Optional

# Package Imports
from gmdkit.serialization.mixins import DataclassDecoderMixin
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.serialization.type_cast import to_string
from gmdkit.models.prop.replay_data.persistent import PersistentData


@dataclass_decoder(slots=True, separator=',', from_array=False, auto_key=lambda key, value: str(value))
class CheckpointData(DataclassDecoderMixin):
    
    seed: int
    todo_2: int
    retries: int
    time_step: int # 480 tickrate
    taps: int
    points: int
    time: int # scaled by 10**5
    persistent_data: Optional[PersistentData] = field_decoder(decoder=PersistentData.from_string,encoder=to_string)
    