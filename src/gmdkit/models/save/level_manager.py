# Imports
from typing import Self, TYPE_CHECKING

# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.utils.typing import PathString
from gmdkit.models.level import LevelList
from gmdkit.models.level_pack import LevelPackList
from gmdkit.serialization.type_cast import to_node
from gmdkit.serialization.mixins import PlistDecoderMixin, CompressFileMixin, FilePathMixin
from gmdkit.serialization.functions import dict_cast, from_node_wrap, to_node_wrap, read_plist, write_plist
from gmdkit.constants.paths.save import LOCAL_LEVELS_PATH
from gmdkit.mappings import lvl_save


LEVEL_SAVE_DECODER = {
    "LLM_01": LevelList.from_node,
    "LLM_02": from_node_wrap(int),
    "LLM_03": LevelPackList.from_node    
    }

LEVEL_SAVE_ENCODER = {
    "LLM_01": to_node,
    "LLM_02": to_node_wrap(int),
    "LLM_03": to_node   
    }

ALLOW_KWARGS = {"LLM_01","LLM_03"}

class LevelSave(FilePathMixin,CompressFileMixin,PlistDecoderMixin,DictClass):
    
    DEFAULT_PATH = LOCAL_LEVELS_PATH
    COMPRESSED = True
    COMPRESSION = "gzip"
    CYPHER = bytes([11])
    
    DECODER = staticmethod(dict_cast(LEVEL_SAVE_DECODER,default=read_plist,allow_kwargs=ALLOW_KWARGS))
    ENCODER = staticmethod(dict_cast(LEVEL_SAVE_ENCODER,default=write_plist,allow_kwargs=ALLOW_KWARGS))
    
    if TYPE_CHECKING:
        @classmethod
        def from_file(cls, path:PathString, load_level_data:bool=False, load_level_content:bool=False, load_pack_data:bool=True, **kwargs) -> Self: ...
        
        def to_file(self, path:PathString, save_level_data:bool=False, save_level_content:bool=False, save_pack_data:bool=True, **kwargs): ...


if __name__ == "__main__":
    import time

    _start = time.perf_counter()
    level_data = LevelSave.from_file()
    levels = level_data[lvl_save.LEVELS]
    binary = level_data[lvl_save.BINARY]
    lists = level_data[lvl_save.LISTS]
    
    _end = time.perf_counter()
    print(f"Load took {_end - _start:.6f} seconds")