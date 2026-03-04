# Imports
from typing import Self, Optional

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.serialization.mixins import (
    DictDecoderMixin, 
    ArrayDecoderMixin,
    PlistDecoderMixin,
    FilePathMixin,
    DelimiterMixin,
    FileStringMixin,
    LoadPlistContentMixin
    )
from gmdkit.serialization.type_cast import serialize, to_numkey
from gmdkit.serialization.functions import dict_cast, write_plist, kv_wrap
from gmdkit.casting.object_props import PROPERTY_DECODERS, PROPERTY_ENCODERS
from gmdkit.defaults.objects import OBJECT_DEFAULT


class Object(DelimiterMixin,DictDecoderMixin,DictClass):
    
    SEPARATOR = ","
    END_DELIMITER = ";"
    DECODER = staticmethod(dict_cast(PROPERTY_DECODERS,key_start=to_numkey))
    ENCODER = staticmethod(dict_cast(PROPERTY_ENCODERS,key_end=str,default=serialize))
    
    @classmethod
    def default(cls, object_id:int) -> Self:
                
        string = OBJECT_DEFAULT.get(object_id, f"1,{object_id},2,0,3,0;")
        
        return cls.from_string(string)
    
    
class ObjectList(ArrayDecoderMixin,ListClass):
    
    SEPARATOR = ";"
    KEEP_SEPARATOR = True
    DECODER = Object.from_string
    ENCODER = Object.to_string
    

class ObjectGroup(FileStringMixin):
    
    __slots__ = ("string","objects")
    
    def __init__(self, string:Optional[str]=None):
        self.string = string or str()
    
    
    def load(self, string:Optional[str]=None) -> ObjectList:
        
        string = self.string if string is None else string
        
        self.objects = ObjectList.from_string(string)
        
        return self.objects
    
    
    def save(self, objects:Optional[ObjectList]=None) -> str:
        objects = getattr(self, "objects", None) if objects is None else objects
    
        if objects is None:
            return self.string
    
        self.string = objects.to_string()
        
        return self.string
    
    
    @classmethod
    def from_string(cls, string:str, load_content:bool=True):
        
        new = cls(string)
        
        if load_content:
            new.load()
            
        return new
    
    
    def to_string(self, save_content:bool=True):
        
        if save_content:
            self.save()
        
        return self.string


class ObjectGroupDict(LoadPlistContentMixin,FilePathMixin,PlistDecoderMixin,DictClass):
    DECODER = staticmethod(kv_wrap(int,ObjectGroup))
    ENCODER = staticmethod(kv_wrap(str,lambda x: write_plist(x.string)))
    EXTENSION = "plist"
    LOAD_CONTENT = False
    
    def _name_fallback_(self):
        return "objectgroup"