# Imports
from typing import Any

# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.serialization.mixins import (
    CompressFileMixin,
    FilePathMixin,
    DefaultPathMixin
    )
from gmdkit.constants.paths.save import LOCAL_LEVELS_PATH
from gmdkit.casting.level_save_loader import FieldLoaderMixin


class LevelSave(
        DefaultPathMixin,
        FilePathMixin,
        CompressFileMixin,
        FieldLoaderMixin,
        DictClass[str,Any]
        ):

    COMPRESSED = True
    COMPRESSION = "gzip"
    CYPHER = bytes([11])
    EXTENSION = "dat"
    DEFAULT_PATH = LOCAL_LEVELS_PATH
    LOAD_CONTENT = False


    def _name_fallback_(self):
        return "CCLocalLevels"


if __name__ == "__main__":
    from gmdkit.utils.classes import Timer

    _t = Timer(start=True)
    level_data = LevelSave.from_default_path()
    print("Load took", _t.end(), "seconds")
    levels = level_data.levels
    binary = level_data.binary
    lists = level_data.lists
