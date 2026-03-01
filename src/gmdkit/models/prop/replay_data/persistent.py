# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.serialization.mixins import DataclassDecoderMixin, DictDecoderMixin
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.models.prop.replay_data.timer import TimerData


class ItemDict(DictDecoderMixin,DictClass):
    
    SEPARATOR = "|"
    DECODER = staticmethod(lambda k, v:(int(k),int(v)))
    ENCODER = staticmethod(lambda k, v:(str(k),str(v))) 


class TimerDict(ItemDict):
    
    DECODER = staticmethod(lambda k, v: (int(k),TimerData.from_string(v)))
    ENCODER = staticmethod(lambda k, v: (str(k),v.to_string()))


@dataclass_decoder(slots=True, separator='@', from_array=True, default_optional=True)
class PersistentData(DataclassDecoderMixin):
    
    items: ItemDict = field_decoder(default_factory=ItemDict,decoder=ItemDict.from_string,encoder=ItemDict.to_string)
    timers: TimerDict = field_decoder(default_factory=TimerDict,decoder=TimerDict.from_string,encoder=ItemDict.to_string)