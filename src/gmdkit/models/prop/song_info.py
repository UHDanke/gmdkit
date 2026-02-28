# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.utils.typing import Element
from gmdkit.serialization.mixins import PlistDecoderMixin, FilePathMixin


class SongInfo(PlistDecoderMixin,DictClass):
    ENCODER_KEY = 6
    
def to_song(key:str, node:Element, **kwargs) -> tuple[int,SongInfo]:
    return int(key), SongInfo.from_node(node=node, **kwargs)

def from_song(key:int, song_info:SongInfo, **kwargs) -> tuple[str,Element]:
    return str(key), song_info.to_node(**kwargs)

class SongInfoList(FilePathMixin,PlistDecoderMixin,DictClass):
    DECODER = staticmethod(to_song)
    ENCODER = staticmethod(from_song)
    EXTENSION = "plist"
    
    def _name_fallback_(self):
        return "songinfo"