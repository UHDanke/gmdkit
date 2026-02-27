# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.serialization.mixins import PlistDecoderMixin, CompressFileMixin, FilePathMixin
from gmdkit.constants.paths.save import GAME_MANAGER_PATH
from gmdkit.serialization.type_cast import to_node as to_node_func
from gmdkit.models.level import LevelMapping


GAME_SAVE_DECODER = {
    "GLM_01": LevelMapping.from_node, 
    }

GAME_SAVE_ENCODER = {
    "GLM_01": to_node_func,
    }

    
class GameSave(FilePathMixin,CompressFileMixin,PlistDecoderMixin,DictClass):

    DEFAULT_PATH = GAME_MANAGER_PATH
    COMPRESSED = True
    COMPRESSION = "gzip"
    CYPHER = bytes([11])

# GLM_01: LevelMapping



if __name__ == "__main__":
    
    import time

    _start = time.perf_counter()
    game_data = GameSave.from_file()
    _end = time.perf_counter()
    print(f"Load took {_end - _start:.6f} seconds")