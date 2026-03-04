# Imports
from typing import Any

# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.serialization.mixins import PlistDecoderMixin, FilePathMixin
from gmdkit.serialization.functions import kv_wrap


class SongInfo(PlistDecoderMixin,DictClass[str,Any]):
    ENCODER_KEY = 6


class SongInfoList(FilePathMixin,PlistDecoderMixin,DictClass[int,SongInfo]):
    DECODER = staticmethod(kv_wrap(int,SongInfo.from_node))
    ENCODER = staticmethod(kv_wrap(str,SongInfo.to_node))
    EXTENSION = "plist"
    
    def _name_fallback_(self):
        return "songinfo"