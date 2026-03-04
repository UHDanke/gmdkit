# Imports
from typing import Any

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.serialization.mixins import PlistDecoderMixin, FilePathMixin, FolderLoaderMixin
from gmdkit.serialization.functions import dict_cast, from_node_dict, to_node_dict, read_plist, write_plist
from gmdkit.casting.list_props import LIST_ENCODERS, LIST_DECODERS, LIST_NODES
from gmdkit.mappings import list_prop


class LevelPack(FilePathMixin,PlistDecoderMixin,DictClass[str,Any]):
    
    DECODER = staticmethod(dict_cast(from_node_dict(LIST_DECODERS,exclude=LIST_NODES),default=read_plist))
    ENCODER = staticmethod(dict_cast(to_node_dict(LIST_ENCODERS,exclude=LIST_NODES),default=write_plist))
    ENCODER_KEY = 12
    EXTENSION = "gmdl"

    def _name_fallback_(self):
        container = self.CONTAINER
        data = self if container is None else getattr(self, container)
        return data[list_prop.NAME]


class LevelPackList(FolderLoaderMixin,PlistDecoderMixin,ListClass[LevelPack]):
    
    __slots__ = ()
    
    DECODER = LevelPack.from_node
    ENCODER = LevelPack.to_node
    IS_ARRAY = True
    EXTENSION = "plist"
    
    FOLDER_DECODER = LevelPack.from_file
    FOLDER_ENCODER = LevelPack.to_file
    FOLDER_EXTENSION = "gmdl"
