# Imports
from typing import Self, TYPE_CHECKING

# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.utils.typing import PathString
from gmdkit.serialization.mixins import (
    PlistDecoderMixin, 
    CompressFileMixin, 
    FilePathMixin, 
    DefaultPathMixin
    )
from gmdkit.serialization.functions import dict_cast, read_plist, write_plist
from gmdkit.constants.paths.save import LOCAL_LEVELS_PATH
from gmdkit.mappings import lvl_save
from gmdkit.casting.level_save import LEVEL_SAVE_DECODER, LEVEL_SAVE_ENCODER


ALLOW_KWARGS = {"LLM_01","LLM_03"}


class LevelSave(DefaultPathMixin,FilePathMixin,CompressFileMixin,PlistDecoderMixin,DictClass):
    
    DECODER = staticmethod(dict_cast(LEVEL_SAVE_DECODER,default=read_plist,allow_kwargs=ALLOW_KWARGS))
    ENCODER = staticmethod(dict_cast(LEVEL_SAVE_ENCODER,default=write_plist,allow_kwargs=ALLOW_KWARGS))
    COMPRESSED = True
    COMPRESSION = "gzip"
    CYPHER = bytes([11])
    EXTENSION = "dat"
    DEFAULT_PATH = LOCAL_LEVELS_PATH
    
    def _name_fallback_(self):
        return "CCLocalLevels"
    
    if TYPE_CHECKING:
        @classmethod
        def from_file(cls, path:PathString, load_level_content:bool=False, **kwargs) -> Self: ...
        
        def to_file(self, path:PathString, save_level_content:bool=False, **kwargs): ...


if __name__ == "__main__":
    import time

    _start = time.perf_counter()
    level_data = LevelSave.from_default_path()
    levels = level_data[lvl_save.LEVELS]
    binary = level_data[lvl_save.BINARY]
    lists = level_data[lvl_save.LISTS]
    
    _end = time.perf_counter()
    print(f"Load took {_end - _start:.6f} seconds")