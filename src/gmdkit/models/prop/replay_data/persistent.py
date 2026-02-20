# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.serialization.mixins import DataclassDecoderMixin, DictDecoderMixin
from gmdkit.serialization.decorators import dataclass_decoder, field_decoder
from gmdkit.serialization.type_cast import to_string
from gmdkit.models.prop.replay_data.timer import TimerData


class ItemDict(DictDecoderMixin,DictClass):
    
    SEPARATOR = "|"
    DECODER = lambda key, value, **kwargs: (int(key),int(value))
    ENCODER = lambda key, value, **kwargs: (str(key),str(value))    


class TimerDict(ItemDict):
    
    DECODER = lambda key, value, **kwargs: (int(key),TimerData.from_string(value))
    ENCODER = lambda key, value, **kwargs: (str(key),value.to_string())


@dataclass_decoder(slots=True, separator='@', list_format=True)
class PersistentData(DataclassDecoderMixin):
    
    items: ItemDict = field_decoder(decoder=ItemDict.from_string,encoder=to_string)
    timers: TimerDict = field_decoder(decoder=TimerDict.from_string,encoder=to_string)
    
    
persistent = PersistentData.from_string("1234|4|1235|1000@1236|1236&1251&1&9002&1&9001&0&9003&53&9004&1&1_2_-50|1567|1567&3&1&9002&1&9001&0&9003&48&9004&1&1_2_-50")
