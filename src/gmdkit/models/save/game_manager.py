# Package Imports
from gmdkit.serialization.types import DictClass
from gmdkit.serialization.mixins import PlistDictDecoderMixin, LoadFileMixin
from gmdkit.constants.paths import GAME_MANAGER_PATH


class GameSave(LoadFileMixin,PlistDictDecoderMixin,DictClass):

    DEFAULT_PATH = GAME_MANAGER_PATH
    COMPRESSION = "gzip"
    CYPHER = bytes([11])

    
if __name__ == "__main__":
    game_data = GameSave.from_file()