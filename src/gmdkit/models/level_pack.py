# Imports
from pathlib import Path
from os import PathLike
from glob import glob

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.utils.typing import Node
from gmdkit.serialization.mixins import PlistDecoderMixin, FilePathMixin
from gmdkit.serialization.type_cast import to_plist
from gmdkit.serialization.functions import dict_cast, from_node_dict, to_node_dict, read_plist, write_plist
from gmdkit.casting.list_props import LIST_ENCODERS, LIST_DECODERS
from gmdkit.mappings import list_prop


class LevelPack(FilePathMixin,PlistDecoderMixin,DictClass):
    
    DECODER = staticmethod(dict_cast(from_node_dict(LIST_DECODERS),default=read_plist))
    ENCODER = staticmethod(dict_cast(to_node_dict(LIST_ENCODERS),default=write_plist))
    ENCODER_KEY = 6
    EXTENSION = "gmdl"
    NAME_FALLBACK = staticmethod(lambda self: self[list_prop.NAME])



def to_pack(node:Node, load_pack_data:bool=True, **kwargs):
    return LevelPack.from_node(load_data=load_pack_data)

def from_pack(level:LevelPack,save_pack_data:bool=True, **kwargs):
    return level.to_node(save_data=save_pack_data)
        
class LevelPackList(PlistDecoderMixin,ListClass):
    
    __slots__ = ()
    
    DECODER = LevelPack.from_node
    ENCODER = staticmethod(to_plist)
    
    @classmethod
    def from_folder(cls, path:str|PathLike, extension:str='.gmdl'):
        
        new = cls()
        
        folder_path = str(Path(path) / ('*' + extension))
        
        for file in glob(folder_path):
            level = LevelPack.from_file(file)
            
            new.append(level)
        
        return new