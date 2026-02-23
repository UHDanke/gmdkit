# Package Imports
from gmdkit.serialization.mixins import DataclassDecoderMixin, DelimiterMixin
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.serialization.type_cast import to_string
from gmdkit.models.prop.replay_data.persistent import PersistentData


@dataclass_decoder(slots=True, separator=',', from_array=False, auto_key=lambda key, value: str(value+1))
class CheckpointData(DelimiterMixin,DataclassDecoderMixin):
    
    seed: int
    current_retries: int
    total_retries: int
    time_step: int
    taps: int
    points: int
    time: float = field_decoder(decoder=lambda string: int(string) / 100000, encoder=lambda value: str(int(value * 100000)))
    persistent_data: PersistentData = field_decoder(decoder=PersistentData.from_string,encoder=to_string)

CheckpointData.END_DELIMITER = ","