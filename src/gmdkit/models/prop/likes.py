# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.serialization.functions import kv_wrap, from_node_wrap, to_node_wrap
from gmdkit.serialization.type_cast import to_bool, from_bool
from gmdkit.serialization.mixins import PlistDecoderMixin, DataclassDecoderMixin, DelimiterMixin
from gmdkit.serialization.functions import dataclass_decoder, field_decoder


@dataclass_decoder(slots=True, frozen=True, separator="_", from_array=True)
class LikeData(DelimiterMixin,DataclassDecoderMixin):
    START_DELIMITER = "like_"

    m_1: int # like type?
    m_2: int # level id?
    m_3: bool # like / dislike?
    m_4: int # level id again?


class LikeDict(PlistDecoderMixin,DictClass[LikeData,bool]):
    DECODER = staticmethod(kv_wrap(LikeData.from_string, from_node_wrap(to_bool), None))
    ENCODER = staticmethod(kv_wrap(LikeData.to_string, to_node_wrap(from_bool), None))
