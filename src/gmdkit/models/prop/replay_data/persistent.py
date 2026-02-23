# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.serialization.mixins import DataclassDecoderMixin, DictDecoderMixin
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.serialization.type_cast import to_string, args_to_int, args_to_str
from gmdkit.models.prop.replay_data.timer import TimerData


class ItemDict(DictDecoderMixin,DictClass):
    
    SEPARATOR = "|"
    DECODER = staticmethod(args_to_int)
    ENCODER = staticmethod(args_to_str)    


class TimerDict(ItemDict):
    
    DECODER = staticmethod(lambda key, value: (int(key),TimerData.from_string(value)))
    ENCODER = staticmethod(lambda key, value: (str(key),value.to_string()))


@dataclass_decoder(slots=True, separator='@', from_array=True, default_optional=True)
class PersistentData(DataclassDecoderMixin):
    
    items: ItemDict = field_decoder(default_factory=ItemDict,decoder=ItemDict.from_string,encoder=to_string)
    timers: TimerDict = field_decoder(default_factory=TimerDict,decoder=TimerDict.from_string,encoder=to_string)