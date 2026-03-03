# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.models.object import Object, ObjectList
from gmdkit.serialization.mixins import PlistDecoderMixin, FilePathMixin, LoadPlistContentMixin, FolderLoaderMixin
from gmdkit.serialization.functions import (
    dict_cast, from_node_dict, to_node_dict, read_plist, write_plist, get_load_keys, kv_wrap, args_wrap
    )
from gmdkit.casting.level_props import LEVEL_ENCODERS, LEVEL_DECODERS, LEVEL_TYPES
from gmdkit.defaults.level import LEVEL_DEFAULT
from gmdkit.mappings import lvl_prop


class Level(LoadPlistContentMixin,FilePathMixin,PlistDecoderMixin,DictClass):
    
    DECODER = staticmethod(dict_cast(from_node_dict(LEVEL_DECODERS),default=read_plist))
    ENCODER = staticmethod(dict_cast(to_node_dict(LEVEL_ENCODERS),default=write_plist))
    ENCODER_KEY = 4
    EXTENSION = "gmd"
    SELECTORS = get_load_keys(LEVEL_TYPES)

    
    def _name_fallback_(self):
        container = self.CONTAINER
        data = self if container is None else getattr(self, container)
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
    
    @classmethod
    def default(cls, name:str, **kwargs):
        
        new = cls.from_string(LEVEL_DEFAULT,**kwargs)        
        new[lvl_prop.NAME] = name
                
        return new
   
    
class LevelList(LoadPlistContentMixin,FolderLoaderMixin,FilePathMixin,PlistDecoderMixin,ListClass):
    
    __slots__ = ()
    
    DECODER = Level.from_node
    ENCODER = Level.to_node
    IS_ARRAY = True
    EXTENSION = "plist"
    
    FOLDER_DECODER = staticmethod(args_wrap(Level.from_file,1))
    FOLDER_ENCODER = staticmethod(args_wrap(Level.to_file,2))
    FOLDER_EXTENSION = "gmd"
    
    LOAD_CONTENT = False


class LevelMapping(LoadPlistContentMixin,PlistDecoderMixin,DictClass):
    DECODER = staticmethod(kv_wrap(int, Level.from_node))   
    ENCODER = staticmethod(kv_wrap(str, Level.to_node))  
    LOAD_CONTENT = False
    