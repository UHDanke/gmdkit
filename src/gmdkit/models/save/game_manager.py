# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.serialization.mixins import (
    PlistDecoderMixin, 
    CompressFileMixin, 
    FilePathMixin, 
    DefaultPathMixin,
    LoadPlistContentMixin
    )
from gmdkit.constants.paths.save import GAME_MANAGER_PATH
from gmdkit.serialization.type_cast import to_numkey
from gmdkit.serialization.functions import dict_cast, from_node_dict, to_node_dict, read_plist, write_plist
from gmdkit.casting.game_save import GAME_SAVE_DECODERS, GAME_SAVE_ENCODERS, GAME_SAVE_NODES


GAME_SAVE_KWARGS = {}


class GameSave(DefaultPathMixin,FilePathMixin,LoadPlistContentMixin,CompressFileMixin,PlistDecoderMixin,DictClass):
    DECODER = staticmethod(dict_cast(from_node_dict(GAME_SAVE_DECODERS,exclude=GAME_SAVE_NODES),key_start=to_numkey,default=read_plist,allow_kwargs=GAME_SAVE_KWARGS))
    ENCODER = staticmethod(dict_cast(to_node_dict(GAME_SAVE_ENCODERS,exclude=GAME_SAVE_NODES),key_end=str,default=write_plist,allow_kwargs=GAME_SAVE_KWARGS))
    COMPRESSED = True
    COMPRESSION = "gzip"
    CYPHER = bytes([11])
    EXTENSION = "dat"
    DEFAULT_PATH = GAME_MANAGER_PATH
    LOAD_CONTENT = False
    
    def _name_fallback_(self):
        return "CCGameManager"
    

if __name__ == "__main__":
    
    import time

    _start = time.perf_counter()
    game_data = GameSave.from_default_path()
    _end = time.perf_counter()
    print(f"Load took {_end - _start:.6f} seconds")