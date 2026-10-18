# Package Imports
from gmdkit.serialization.functions import dataclass_decoder
from gmdkit.serialization.mixins import DataclassDecoderMixin


@dataclass_decoder(slots=True, separator=",", from_array=True)
class EditorStats(DataclassDecoderMixin):
    unk_1: int = 0
    objects_placed: int = 0
    unk_3: int = 0
    objects_deleted: int = 0
    unk_5: int = 0
    unk_6: int = 0
    unk_7: int = 0
    unk_8: int = 0
    unk_9: int = 0
    active_edit_time_ms: int = 0
    unk_11: int = 0
    unk_12: int = 0
    unk_13: int = 0
    unk_14: int = 0
    unk_15: int = 0
    unk_16: int = 0
    unk_17: int = 0
    unk_18: int = 0
    inputs: int = 0
    saves: int = 0
    time_created: int = 0
    unk_22: int = 0
    unk_23: int = 0