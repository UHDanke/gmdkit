# Imports
from typing import Any

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.models.object import Object, ObjectList
from gmdkit.models.prop.gzip import ObjectString
from gmdkit.serialization.mixins import FilePathMixin, PlistLoaderMixin, FolderLoaderMixin, DictDefaultsMixin
from gmdkit.serialization.functions import (
    dict_cast, from_node_dict, to_node_dict, read_plist, write_plist, get_load_keys, kv_wrap, args_wrap
    )
from gmdkit.casting.level_props import LEVEL_ENCODERS, LEVEL_DECODERS, LEVEL_TYPES
from gmdkit.defaults.level import LEVEL_DEFAULT
from gmdkit.mappings import lvl_prop


class Level(FilePathMixin,DictDefaultsMixin,PlistLoaderMixin,DictClass[str,Any]):
    
    DECODER = staticmethod(dict_cast(from_node_dict(LEVEL_DECODERS),default=read_plist))
    ENCODER = staticmethod(dict_cast(to_node_dict(LEVEL_ENCODERS),default=write_plist))
    TYPES = LEVEL_TYPES
    ENCODER_KEY = 4
    EXTENSION = "gmd"
    SELECTORS = get_load_keys(LEVEL_TYPES)

    
    def _name_fallback_(self):
        container = self.CONTAINER
        data = self if container is None else getattr(self, container)
        name = data.get(lvl_prop.NAME)
        if name is None:
            return str(data[lvl_prop.ID])
        return name   
    
    @property
    def start(self) -> Object:
        objstr = self.setdefault(lvl_prop.OBJECT_STRING, ObjectString())
                
        if not hasattr(objstr, "start"):
            objstr.load()

        return getattr(objstr, "start")
    
    @start.setter
    def start(self, value: Object):
        objstr = self.setdefault(lvl_prop.OBJECT_STRING, ObjectString())
        
        if not hasattr(objstr, "start"):
            objstr.load()
            
        setattr(objstr, "start", value)
        
    @property
    def objects(self) -> ObjectList:
        objstr = self.setdefault(lvl_prop.OBJECT_STRING, ObjectString())
        
        if not hasattr(objstr, "objects"):
            objstr.load()

        return getattr(objstr, "objects")
    
    @objects.setter
    def objects(self, value: ObjectList):
        objstr = self.setdefault(lvl_prop.OBJECT_STRING, ObjectString())
        
        if not hasattr(objstr, "objects"):
            objstr.load()
            
        setattr(objstr, "objects", value)
        
    @classmethod
    def default(cls, name:str, **kwargs):
        
        new = cls.from_string(LEVEL_DEFAULT,**kwargs)        
        new[lvl_prop.NAME] = name
                
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
    