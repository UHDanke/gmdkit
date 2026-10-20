# Imports
from typing import Any

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.serialization.mixins import PlistDecoderMixin, FilePathMixin, ArrayDecoderMixin, DictDecoderMixin, DataclassDecoderMixin
from gmdkit.serialization.functions import kv_wrap
from gmdkit.serialization.functions import dataclass_decoder, field_decoder


class SongInfo(PlistDecoderMixin,DictClass[str,Any]):
    ENCODER_KEY = 6


class SongInfoList(FilePathMixin,PlistDecoderMixin,DictClass[int,SongInfo]):
    DECODER = staticmethod(kv_wrap(int,SongInfo.from_node))
    ENCODER = staticmethod(kv_wrap(str,SongInfo.to_node))
    EXTENSION = "plist"
    
    def _name_fallback_(self):
        return "songinfo"

@dataclass_decoder(slots=True, from_array=True, separator=":")
class RecentSFX(DataclassDecoderMixin):
    sfx_id: int = 0
    custom_id: int = field_decoder(default=0, optional=True)
 
 
class RecentSFXList(ArrayDecoderMixin, ListClass[RecentSFX]):
    
    __slots__ = ()
 
    SEPARATOR = ","
    DECODER = RecentSFX.from_string
    ENCODER = RecentSFX.to_string
 
 
class UseCountDict(DictDecoderMixin, DictClass[int, int]):
    SEPARATOR = ","
    PAIR_SEPARATOR = ":"
    DECODER = staticmethod(lambda k, v: (int(k), int(v)))
    ENCODER = staticmethod(lambda k, v: (str(k), str(v)))