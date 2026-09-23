# Imports
from typing import Any

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.serialization.mixins import PlistDecoderMixin, FilePathMixin, FolderLoaderMixin
from gmdkit.casting.list_loader import FieldLoaderMixin


class LevelPack(FilePathMixin,FieldLoaderMixin,DictClass[str,Any]):

    ENCODER_KEY = 12
    EXTENSION = "gmdl"

    def _name_fallback_(self):
        return self.name


class LevelPackList(FolderLoaderMixin,PlistDecoderMixin,ListClass[LevelPack]):

    __slots__ = ()

    DECODER = LevelPack.from_node
    ENCODER = LevelPack.to_node
    IS_ARRAY = True
    EXTENSION = "plist"

    FOLDER_DECODER = LevelPack.from_file
    FOLDER_ENCODER = LevelPack.to_file
    FOLDER_EXTENSION = "gmdl"
