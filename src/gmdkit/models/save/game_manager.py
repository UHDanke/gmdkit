# Package Imports
from gmdkit.models.level import LevelList
from gmdkit.serialization.types import DictClass
from gmdkit.serialization.mixins import PlistDictDecoderMixin, CompressFileMixin
from gmdkit.constants.paths.save import GAME_MANAGER_PATH


def levels_from_dict(data, **kwargs):
    return LevelList.from_plist(list(data.values()), **kwargs)
    
def levels_to_dict(level_list, **kwargs):
    keys = (lvl['k1'] for lvl in level_list)
    return dict(keys,level_list.to_plist(**kwargs))

    
class GameSave(CompressFileMixin,PlistDictDecoderMixin,DictClass):

    DEFAULT_PATH = GAME_MANAGER_PATH
    COMPRESSION = "gzip"
    CYPHER = bytes([11])

    
if __name__ == "__main__":
    game_data = GameSave.from_file()