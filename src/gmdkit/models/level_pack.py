# Imports
from typing import TYPE_CHECKING, Self

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.utils.typing import PathString, Element
from gmdkit.serialization.mixins import PlistDecoderMixin, FilePathMixin, FolderLoaderMixin
from gmdkit.serialization.functions import dict_cast, from_node_dict, to_node_dict, read_plist, write_plist
from gmdkit.casting.list_props import LIST_ENCODERS, LIST_DECODERS
from gmdkit.mappings import list_prop


class LevelPack(FilePathMixin,PlistDecoderMixin,DictClass):
    
    DECODER = staticmethod(dict_cast(from_node_dict(LIST_DECODERS,exclude={'k97'}),default=read_plist))
    ENCODER = staticmethod(dict_cast(to_node_dict(LIST_ENCODERS,exclude={'k97'}),default=write_plist))
    ENCODER_KEY = 6
    EXTENSION = "gmdl"

    def _name_fallback_(self):
        container = self.CONTAINER
        
        if container is None:
            data = self
        else:
            data = getattr(self, container)
            
        return data[list_prop.NAME]
    
    if TYPE_CHECKING:
        @classmethod
        def from_file(cls, path:PathString, load_data:bool=True, **kwargs) -> Self: ...
    
        def to_file(cls, path:PathString, save_data:bool=True, **kwargs): ...


def to_pack(node:Element, load_pack_data:bool=True, **kwargs) -> LevelPack:
    return LevelPack.from_node(node=node,load_data=load_pack_data)

def from_pack(pack:LevelPack, save_pack_data:bool=True, **kwargs) -> Element:
    return pack.to_node(save_data=save_pack_data)
        
def pack_from_file(path:PathString, load_pack_data:bool=True, **kwargs) -> LevelPack:
    return LevelPack.from_file(load_data=load_pack_data)

def pack_to_file(pack:LevelPack,path:PathString, save_pack_data:bool=True, **kwargs) -> Element:
    return pack.to_file(path=path,save_data=save_pack_data)


class LevelPackList(FolderLoaderMixin,PlistDecoderMixin,ListClass):
    
    __slots__ = ()
    
    DECODER = staticmethod(to_pack)
    ENCODER = staticmethod(from_pack)
    IS_ARRAY = True
    EXTENSION = "plist"
    
    FOLDER_DECODER = staticmethod(pack_from_file)
    FOLDER_ENCODER = staticmethod(pack_to_file)
    FOLDER_EXTENSION = "gmdl"
    

    if TYPE_CHECKING:
        @classmethod
        def from_file(cls, path:PathString, load_pack_data:bool=True, **kwargs) -> Self: ...
        
        def to_file(self, path:PathString, save_pack_data:bool=True, **kwargs): ...


        @classmethod
        def from_folder(cls, path:PathString, load_pack_data:bool=True, **kwargs) -> Self: ...
        
        def to_folder(self, path:PathString, save_pack_data:bool=True, **kwargs): ...
        
    