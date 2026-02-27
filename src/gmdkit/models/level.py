# Imports
from typing import Self, TYPE_CHECKING

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.utils.typing import PathString, Element
from gmdkit.models.object import Object, ObjectList
from gmdkit.serialization.mixins import PlistDecoderMixin, FilePathMixin, LoadContentMixin, FolderLoaderMixin
from gmdkit.serialization.functions import dict_cast, from_node_dict, to_node_dict, read_plist, write_plist
from gmdkit.casting.level_props import LEVEL_ENCODERS, LEVEL_DECODERS, LEVEL_TYPES
from gmdkit.defaults.level import LEVEL_DEFAULT
from gmdkit.mappings import lvl_prop


LOAD_KEYS = {k for k, v in LEVEL_TYPES.items() if hasattr(v, "load") and hasattr(v, "save")}


class Level(LoadContentMixin,FilePathMixin,PlistDecoderMixin,DictClass):
    
    DECODER = staticmethod(dict_cast(from_node_dict(LEVEL_DECODERS),default=read_plist))
    ENCODER = staticmethod(dict_cast(to_node_dict(LEVEL_ENCODERS),default=write_plist))
    ENCODER_KEY = 4
    EXTENSION = "gmd"
    CONTENT_KEYS = {k for k, v in LEVEL_TYPES.items() if hasattr(v, "load") and hasattr(v, "save")}
    
    
    if TYPE_CHECKING:
        @classmethod
        def from_file(cls, path:PathString, load_data:bool=True, load_content:bool=True, **kwargs) -> Self: ...
    
        def to_file(cls, path:PathString, save_data:bool=True, save_content:bool=True, **kwargs): ...
    
    
    def _name_fallback_(self):
        container = self.CONTAINER
        
        if container is None:
            data = self
        else:
            data = getattr(self, container)
            
        return data[lvl_prop.NAME]    
    
    @property
    def start(self) -> Object:
        objstr = self.get(lvl_prop.OBJECT_STRING)
        
        if objstr is None:
            raise RuntimeError("Object string is missing.")
        
        if not hasattr(objstr, "start"):
            raise RuntimeError("Object string is not loaded.")

        return getattr(objstr, "start")
    
    
    @property
    def objects(self) -> ObjectList:
        objstr = self.get(lvl_prop.OBJECT_STRING)
        
        if objstr is None:
            raise RuntimeError("Object string is missing.")
        
        if not hasattr(objstr, "objects"):
            raise RuntimeError("Object string is not loaded.")

        return getattr(objstr, "objects")
    
    # TODO REDO
    @classmethod
    def default(cls, name:str,load:bool=True):
        
        data = LEVEL_DEFAULT.copy()        
        data[lvl_prop.NAME] = name
                
        return cls.from_plist(data, load=load)


def to_level(node:Element, load_level_data:bool=True, load_level_content:bool=False, **kwargs) -> Level:
    return Level.from_node(node=node,load_data=load_level_data,load_content=load_level_content)

def from_level(level:Level,save_level_data:bool=True, save_level_content:bool=False, **kwargs) -> Element:
    return level.to_node(save_data=save_level_data,save_content=save_level_content)

def level_from_file(path:PathString, load_level_data:bool=True, load_level_content:bool=False, **kwargs) -> Level:
    return Level.from_file(load_data=load_level_data,load_content=load_level_content)

def level_to_file(level:Level,path:PathString, save_level_data:True=False, save_level_content:bool=False, **kwargs) -> Element:
    return level.to_file(path=path,save_data=save_level_data,save_content=save_level_content)


class LevelList(FolderLoaderMixin,FilePathMixin,PlistDecoderMixin,ListClass):
    
    __slots__ = ()
    
    DECODER = staticmethod(to_level)
    ENCODER = staticmethod(from_level)
    IS_ARRAY = True
    EXTENSION = "plist"
    
    FOLDER_DECODER = staticmethod(level_from_file)
    FOLDER_ENCODER = staticmethod(level_to_file)
    FOLDER_EXTENSION = "gmd"
    

    if TYPE_CHECKING:
        @classmethod
        def from_file(cls, path:PathString, load_level_data:bool=False, load_level_content:bool=False, **kwargs) -> Self: ...
        
        def to_file(self, path:PathString, save_level_data:bool=False, save_level_content:bool=False, **kwargs): ...


        @classmethod
        def from_folder(cls, path:PathString, load_level_data:bool=False, load_level_content:bool=False, **kwargs) -> Self: ...
        
        def to_folder(self, path:PathString, save_level_data:bool=False, save_level_content:bool=False, **kwargs): ...
        
    