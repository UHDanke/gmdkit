# Imports
from typing import Self, Callable
from os import PathLike

# Package Imports
from gmdkit.models.types import ListClass, DictClass
from gmdkit.models.serialization import DictDecoderMixin, ArrayDecoderMixin, DelimiterMixin, dict_cast, decode_string, encode_string, serialize
from gmdkit.casting.object_props import PROPERTY_DECODERS, PROPERTY_ENCODERS
from gmdkit.defaults.objects import OBJECT_DEFAULT


class Object(DelimiterMixin,DictDecoderMixin,DictClass):
    
    __slots__ = ()
    
    SEPARATOR = ","
    END_DELIMITER = ";"
    DECODER = staticmethod(dict_cast(PROPERTY_DECODERS,numkey=True))
    ENCODER = staticmethod(dict_cast(PROPERTY_ENCODERS,default=serialize))
    DEFAULTS = OBJECT_DEFAULT

    
    @classmethod
    def default(cls, object_id:int, decoder:Callable=None) -> Self:
        
        decoder = decoder or cls.DECODER
        
        data = cls.DEFAULTS.get(object_id,{})
        
        return cls(decoder(k, v) for k, v in data.items())
    
    
class ObjectList(ArrayDecoderMixin,ListClass):
    
    __slots__ = ()
    
    SEPARATOR = ";"
    END_SEP = True
    DECODER = Object.from_string
    ENCODER = staticmethod(lambda x, **kwargs: x.to_string(**kwargs))
    
    
    @classmethod
    def from_string(cls, string, encoded:bool=False, **kwargs):
        
        if encoded:
            string = decode_string(string)
            
        return super().from_string(string, **kwargs)


    def to_string(self, encoded:bool=False, **kwargs) -> str:
                
        string = super().to_string(**kwargs)
        
        if encoded:
            string = encode_string(string)
            
        return string
    
    
    @classmethod
    def from_file(cls, path:str|PathLike, encoded:bool=False) -> Self:
        
        with open(path, "r") as file:
            string = file.read()
            
            return cls.from_string(string,encoded=encoded)


    def to_file(self, path:str|PathLike, encoded:bool=False):
        
        with open(path, "w") as file:
            string = self.to_string(encoded=encoded)
            
            file.write(string)