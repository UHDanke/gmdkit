# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.serialization.mixins import PlistDecoderMixin, CompressFileMixin, FilePathMixin
from gmdkit.constants.paths.save import GAME_MANAGER_PATH
from gmdkit.serialization.type_cast import to_node, to_numkey, to_string
from gmdkit.serialization.functions import dict_cast, from_node_dict, to_node_dict, read_plist, write_plist
from gmdkit.models.level import LevelMapping
from gmdkit.models.level_pack import LevelPackList
from gmdkit.models.template import SmartTemplateList
from gmdkit.models.object import ObjectGroupDict
from gmdkit.models.prop.dpad import MoveButton, JumpButton

GAME_SAVE_DECODERS = {
    "customObjectDict": ObjectGroupDict.from_node,
    "GLM_01": LevelMapping.from_node,
    "GLM_03": LevelMapping.from_node,
    "GLM_10": LevelMapping.from_node,
    "GLM_16": LevelMapping.from_node,
    "GLM_20": SmartTemplateList.from_node,
    "GLM_22": LevelPackList.from_node,
    "dpad01": MoveButton.from_string,
    "dpad02": MoveButton.from_string,
    "dpad03": MoveButton.from_string,
    "dpad04": JumpButton.from_string,
    "dpad05": JumpButton.from_string,
    }

GAME_SAVE_ENCODERS = {
    "customObjectDict": to_node,
    "GLM_01": to_node,
    "GLM_03": to_node,
    "GLM_10": to_node,
    "GLM_16": to_node,
    "GLM_20": to_node,
    "GLM_22": to_node,
    "dpad01": to_string,
    "dpad02": to_string,
    "dpad03": to_string,
    "dpad04": to_string,
    "dpad05": to_string,
    }

GAME_SAVE_NODES = {"customObjectDict","GLM_01","GLM_03","GLM_10","GLM_16","GLM_20","GLM_22"}

GAME_SAVE_KWARGS = {}

    
class GameSave(FilePathMixin,CompressFileMixin,PlistDecoderMixin,DictClass):
    DECODER = staticmethod(dict_cast(from_node_dict(GAME_SAVE_DECODERS,exclude=GAME_SAVE_NODES),key_start=to_numkey,default=read_plist,allow_kwargs=GAME_SAVE_KWARGS))
    ENCODER = staticmethod(dict_cast(to_node_dict(GAME_SAVE_ENCODERS,exclude=GAME_SAVE_NODES),key_end=str,default=write_plist,allow_kwargs=GAME_SAVE_KWARGS))
    COMPRESSED = True
    COMPRESSION = "gzip"
    CYPHER = bytes([11])
    EXTENSION = "dat"
    
    def _name_fallback_(self):
        return "CCGameManager"

if __name__ == "__main__":
    
    import time

    _start = time.perf_counter()
    game_data = GameSave.from_file(GAME_MANAGER_PATH)
    _end = time.perf_counter()
    print(f"Load took {_end - _start:.6f} seconds")