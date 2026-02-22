# Imports
from typing import Self

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.utils.typing import PathString
from gmdkit.serialization.mixins import DictDecoderMixin, ArrayDecoderMixin, DelimiterMixin 
from gmdkit.serialization.functions import decompress_string, compress_string
from gmdkit.serialization.type_cast import dict_cast, serialize, to_string, to_numkey
from gmdkit.casting.object_props import PROPERTY_DECODERS, PROPERTY_ENCODERS
from gmdkit.defaults.objects import OBJECT_DEFAULT


class Object(DelimiterMixin,DictDecoderMixin,DictClass):
    
    SEPARATOR = ","
    END_DELIMITER = ";"
    DECODER = staticmethod(dict_cast(PROPERTY_DECODERS,key_func_start=to_numkey))
    ENCODER = staticmethod(dict_cast(PROPERTY_ENCODERS,key_func_end=str,default=serialize))
    DEFAULTS = OBJECT_DEFAULT

    @classmethod
    def default(cls, object_id:int) -> Self:
                
        string = cls.DEFAULTS.get(object_id, f"1,{object_id},2,0,3,0;")
        
        return cls.from_string(string)
    
    
class ObjectList(ArrayDecoderMixin,ListClass):
    
    SEPARATOR = ";"
    KEEP_SEPARATOR = True
    DECODER = Object.from_string
    ENCODER = staticmethod(to_string)
    
    
    @classmethod
    def from_string(cls, string, compressed:bool=False, **kwargs):
        
        if compressed:
            string = decompress_string(string)
            
        return super().from_string(string, **kwargs)


    def to_string(self, compressed:bool=False, **kwargs) -> str:
                
        string = super().to_string(**kwargs)
        
        if compressed:
            string = compress_string(string)
            
        return string
    
    
    @classmethod
    def from_file(cls, path:PathString, compressed:bool=False) -> Self:
        
        with open(path, "r") as file:
            string = file.read()
            
            return cls.from_string(string,compressed=compressed)


    def to_file(self, path:PathString, compressed:bool=False):
        
        with open(path, "w") as file:
            string = self.to_string(compressed=compressed)
            
            file.write(string)