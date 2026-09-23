# Imports
from typing import Any

# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.serialization.mixins import (
    CompressFileMixin,
    FilePathMixin,
    DefaultPathMixin
    )
from gmdkit.constants.paths.save import GAME_MANAGER_PATH
from gmdkit.casting.game_save_loader import FieldLoaderMixin


class GameSave(DefaultPathMixin,FilePathMixin,CompressFileMixin,FieldLoaderMixin,DictClass[str,Any]):
    COMPRESSED = True
    COMPRESSION = "gzip"
    CYPHER = bytes([11])
    EXTENSION = "dat"
    DEFAULT_PATH = GAME_MANAGER_PATH
    LOAD_CONTENT = False

    def _name_fallback_(self):
        return "CCGameManager"


if __name__ == "__main__":

    from gmdkit.utils.classes import Timer

    _t = Timer(start=True)
    game_data = GameSave.from_default_path()
    print("Load took", _t.end(), "seconds")
