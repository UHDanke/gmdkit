# Imports
from typing import Self, Optional, Any

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.utils.typing import NumKey
from gmdkit.serialization.mixins import ( 
    ArrayDecoderMixin,
    DataclassDecoderMixin,
    FilePathMixin,
    DelimiterMixin,
    FileStringMixin,
    CompressFileMixin,
    PlistLoaderMixin
    )
from gmdkit.serialization.functions import (
    write_plist, kv_wrap, dataclass_decoder, field_decoder
    )
from gmdkit.serialization.classes import LazyString, LazyAttr
from gmdkit.casting.object_loader import FieldLoaderMixin


class Object(DelimiterMixin,FieldLoaderMixin,DictClass[NumKey,Any]):
    
    SEPARATOR = ","
    END_DELIMITER = ";"
    
    @classmethod
    def from_editor(cls, object_id:int, x:float=0, y:float=0) -> Self:
        props = cls.get_frame(object_id)
        extra = props.editor_keys if props is not None else ""
        obj = cls.from_string(f"1,{object_id},2,{x},3,{y}" + (f",{extra}" if extra else "") + ";")
        return obj

    
class ObjectList(ArrayDecoderMixin,ListClass[Object]):
    
    SEPARATOR = ";"
    KEEP_SEPARATOR = True
    DECODER = Object.from_string
    ENCODER = Object.to_string
    
    def difference(self, *obj_lists:Self): # TODO EVALUATE
        to_string = Object.to_string

        obj_set = {
            to_string(obj, sort_keys=True)
            for lst in obj_lists
            for obj in lst
        }

        return self.where(lambda obj: obj.to_string(sort_keys=True) not in obj_set)


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


class ObjectGroupDict(FilePathMixin,PlistLoaderMixin,DictClass[int,ObjectGroup]):
    DECODER = staticmethod(kv_wrap(int,ObjectGroup))
    ENCODER = staticmethod(kv_wrap(str,lambda x: write_plist(x.string)))
    EXTENSION = "plist"
    LOAD_CONTENT = False
    
    def _name_fallback_(self):
        return "objectgroup"


@dataclass_decoder(slots=True, separator=";", from_array=True)
class ObjectString(FilePathMixin,CompressFileMixin,DataclassDecoderMixin):
    start: Object = field_decoder(
        default_factory=Object,
        decoder=Object.from_string,
        encoder=lambda obj: obj.to_string(skip_delimiter=True),
        )
    objects: ObjectList = field_decoder(
        default_factory=ObjectList,
        decoder=ObjectList.from_string,
        encoder=ObjectList.to_string,
        )

ObjectString.MAX_SPLIT = 1
ObjectString.EXTENSION = "txt"
ObjectString.COMPRESSED = True
ObjectString.COMPRESSION = "gzip"

class ObjectStringLazy(LazyString):
    PARSER = ObjectString
    
    start: Object = LazyAttr()
    objects: ObjectList = LazyAttr()