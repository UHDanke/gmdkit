# Imports
from typing import Any

# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.serialization.mixins import (
    CompressFileMixin, 
    FilePathMixin, 
    DefaultPathMixin,
    PlistLoaderMixin
    )
from gmdkit.constants.paths.save import GAME_MANAGER_PATH
from gmdkit.serialization.functions import dict_cast, from_node_dict, to_node_dict, read_plist, write_plist
from gmdkit.casting.game_save import GAME_SAVE_DECODERS, GAME_SAVE_ENCODERS, GAME_SAVE_NODES


GAME_SAVE_KWARGS = set()


class GameSave(DefaultPathMixin,FilePathMixin,CompressFileMixin,PlistLoaderMixin,DictClass[str,Any]):
    DECODER = staticmethod(dict_cast(from_node_dict(GAME_SAVE_DECODERS,exclude=GAME_SAVE_NODES),default=read_plist,allow_kwargs=GAME_SAVE_KWARGS))
    ENCODER = staticmethod(dict_cast(to_node_dict(GAME_SAVE_ENCODERS,exclude=GAME_SAVE_NODES),default=write_plist,allow_kwargs=GAME_SAVE_KWARGS))
    COMPRESSED = True
    COMPRESSION = "gzip"
    CYPHER = bytes([11])
    EXTENSION = "dat"
    DEFAULT_PATH = GAME_MANAGER_PATH
    LOAD_CONTENT = False
    
    def _name_fallback_(self):
        return "CCGameManager"
    

if __name__ == "__main__":
    
    from gmdkit.utils.misc import Timer

    _t = Timer(start=True)
    game_data = GameSave.from_default_path()
    print("Load took", _t.end(), "seconds")