# Imports
from typing import Self, Optional

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.utils.typing import Element
from gmdkit.serialization.mixins import (
    DictDecoderMixin, 
    ArrayDecoderMixin,
    PlistDecoderMixin,
    FilePathMixin,
    DelimiterMixin,
    CompressFileMixin,
    FileStringMixin
    )
from gmdkit.serialization.type_cast import serialize, to_string, to_numkey
from gmdkit.serialization.functions import dict_cast, write_plist
from gmdkit.casting.object_props import PROPERTY_DECODERS, PROPERTY_ENCODERS
from gmdkit.defaults.objects import OBJECT_DEFAULT


class Object(DelimiterMixin,DictDecoderMixin,DictClass):
    
    SEPARATOR = ","
    END_DELIMITER = ";"
    DECODER = staticmethod(dict_cast(PROPERTY_DECODERS,key_start=to_numkey))
    ENCODER = staticmethod(dict_cast(PROPERTY_ENCODERS,key_end=str,default=serialize))
    DEFAULTS = OBJECT_DEFAULT

    @classmethod
    def default(cls, object_id:int) -> Self:
                
        string = cls.DEFAULTS.get(object_id, f"1,{object_id},2,0,3,0;")
        
        return cls.from_string(string)
    
    
class ObjectList(FileStringMixin,CompressFileMixin,ArrayDecoderMixin,ListClass):
    
    SEPARATOR = ";"
    KEEP_SEPARATOR = True
    DECODER = Object.from_string
    ENCODER = staticmethod(to_string)
    COMPRESSED = False
    

class ObjectGroup:
    
    __slots__ = ("string","objects")
    
    def __init__(self, string:Optional[str]=None):
        self.string = string or str()
    
    
    def load(self, string:Optional[str]=None) -> ObjectList:
        
        string = self.string if string is None else string
        
        self.objects = ObjectList.from_string(string)
        
        return self.objects
    
    
    def save(self, objects:Optional[ObjectList]=None) -> str:
        objects = getattr(self, "objects", None) if objects is not None else objects
    
        if objects is None:
            return self.string
    
        self.string = objects.to_string()
        
        return self.string
    
    
    @classmethod
    def from_string(cls, string:str, load_objects:bool=True):
        
        new = cls(string)
        
        if load_objects:
            new.load()
            
        return new
    
    
    def to_string(self, save_objects:bool=True):
        
        if save_objects:
            self.save()
        
        return self.string
    
    
def dict_to_obj_group(key:str, node:Element, load_object_group:bool=True, **kwargs) -> tuple[int,ObjectGroup]:
    return (int(key),ObjectGroup.from_string(node.text,load_objects=load_object_group))

def obj_group_to_dict(key:int, obj_group:ObjectGroup, save_object_group:bool=True, **kwargs) -> tuple[str,Element]:
    return (str(key), write_plist(obj_group.to_string(save_objects=save_object_group)))
    

class ObjectGroupDict(FilePathMixin,PlistDecoderMixin,DictClass):
    DECODER = staticmethod(dict_to_obj_group)
    ENCODER = staticmethod(obj_group_to_dict)
    EXTENSION = "plist"
    
    def _name_fallback_(self):
        return "objectgroup"
    