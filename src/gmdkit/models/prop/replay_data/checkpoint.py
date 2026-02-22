# Imports
from typing import Optional

# Package Imports
from gmdkit.serialization.mixins import DataclassDecoderMixin
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.serialization.type_cast import to_string
from gmdkit.models.prop.replay_data.persistent import PersistentData


@dataclass_decoder(slots=True, separator=',', from_array=False)
class CheckpointData(DataclassDecoderMixin):
    
    seed: int = field_decoder(key="1")
    todo_2: int = field_decoder(key="2")
    retries: int = field_decoder(key="3")
    time_step: int = field_decoder(key="4") # 480 tickrate
    taps: int = field_decoder(key="5")
    points: int = field_decoder(key="6")
    time: int = field_decoder(key="7") # scaled by 10**5
    persistent_data: Optional[PersistentData] = field_decoder(key="8",decoder=PersistentData.from_string,encoder=to_string)
    