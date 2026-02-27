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
    CompressFileMixin
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
    
    
class ObjectList(CompressFileMixin,ArrayDecoderMixin,ListClass):
    
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
    
    def save(self, objects: Optional[ObjectList]=None) -> str:
        objects = getattr(self, "objects", None) if objects is not None else objects
    
        if objects is None:
            return self.string
    
        self.string = objects.to_string()
        
        return self.string


def dict_to_obj_list(key:str, node:Element, load_object_group, **kwargs) -> ObjectGroup:
    
    new = ObjectGroup(node.text)
    
    if load_object_group:
        new.load()
        
    return (int(key),new)

def obj_list_to_dict(key:int, obj_list:ObjectGroup, save_object_group:bool=True, **kwargs) -> Element:
    
    if save_object_group:
        obj_list.save()
        
    return (str(key), write_plist(obj_list.string))
    

class ObjectGroupDict(FilePathMixin,PlistDecoderMixin,DictClass):
    DECODER = staticmethod(dict_to_obj_list)
    ENCODER = staticmethod(obj_list_to_dict)
    EXTENSION = "plist"
    