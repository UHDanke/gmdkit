# Imports
from typing import Any

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.serialization.mixins import (
    FilePathMixin,
    FolderLoaderMixin,
    PlistLoaderMixin
)
from gmdkit.serialization.functions import (
    kv_wrap, args_wrap
)
from gmdkit.defaults.level import LEVEL_DEFAULT
from gmdkit.casting.level_loader import FieldLoaderMixin


class Level(FilePathMixin,FieldLoaderMixin,DictClass[str,Any]):

    ENCODER_KEY = 4
    EXTENSION = "gmd"
    SELECTORS = {"k4", "k34", "k119", "k120"}


    def _name_fallback_(self):
        return str(self.name)

    @classmethod
    def default(cls, name:str, **kwargs):

        new = cls.from_string(LEVEL_DEFAULT,**kwargs)
        new.name = name

        return new


class LevelList(FolderLoaderMixin,FilePathMixin,PlistLoaderMixin,ListClass[Level]):

    __slots__ = ()

    DECODER = Level.from_node
    ENCODER = Level.to_node
    IS_ARRAY = True
    EXTENSION = "plist"

    FOLDER_DECODER = staticmethod(args_wrap(Level.from_file,1))
    FOLDER_ENCODER = staticmethod(args_wrap(Level.to_file,2))
    FOLDER_EXTENSION = Level.EXTENSION

    LOAD_CONTENT = False

    def _name_fallback_(self):
        return "level_list"

class LevelMapping(PlistLoaderMixin,DictClass[int,Level]):
    DECODER = staticmethod(kv_wrap(int, Level.from_node))
    ENCODER = staticmethod(kv_wrap(str, Level.to_node))
    LOAD_CONTENT = False
