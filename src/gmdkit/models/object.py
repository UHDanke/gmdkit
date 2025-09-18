# Imports
from typing import Self, Callable
from os import PathLike

# Package Imports
from gmdkit.models.types import ListClass, DictClass
from gmdkit.models.serialization import DictDecoderMixin, ArrayDecoderMixin, dict_cast, decode_string, encode_string, serialize
from gmdkit.casting.object_props import PROPERTY_DECODERS, PROPERTY_ENCODERS
from gmdkit.defaults.objects import OBJECT_DEFAULT


class Object(DictDecoderMixin,DictClass):
    
    __slots__ = ()
    
    SEPARATOR = ","
    DECODER = staticmethod(dict_cast(PROPERTY_DECODERS,numkey=True))
    ENCODER = staticmethod(dict_cast(PROPERTY_ENCODERS,default=serialize))
    DEFAULTS = OBJECT_DEFAULT
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    
    @classmethod
    def from_string(cls, string, **kwargs) -> Self:
        
        return super().from_string(string=string.rstrip(";"), **kwargs)
    
    
    def to_string(self, **kwargs) -> str:
        
        return super().to_string(**kwargs) + ";"

    
    def update_decode(self, decoder:Callable=None, **kwargs) -> Self:
        
        decoder = decoder or self.DECODER
        
        if decoder is None or not callable(decoder):
            return super().update(**kwargs)
        
        new = {k: v for k, v in (decoder(k, v, **kwargs) for k, v in kwargs.items())}
        
        return super().update(**new)


    @classmethod
    def default(cls, object_id:int, decoder:Callable=None) -> Self:
        
        decoder = decoder or cls.DECODER
        
        data = cls.DEFAULTS.get(object_id,{})
        
        return cls(decoder(k, v) for k, v in data.items())
    
    

class ObjectList(ArrayDecoderMixin,ListClass):
    
    __slots__ = ()
    
    SEPARATOR = ";"
    DECODER = Object.from_string
    ENCODER = staticmethod(lambda x, **kwargs: x.to_string(**kwargs))
    
    def __init__(self, *args):
        
        super().__init__(*args)
    
    
    @classmethod
    def from_string(cls, string, encoded:bool=False, **kwargs):
        
        if encoded:
            string = decode_string(string)
            
        return super().from_string(string.strip(";"), **kwargs)


    def to_string(self, encoded:bool=False, **kwargs) -> str:
                
        string = super().to_string(separator="", **kwargs)
        
        if encoded:
            string = encode_string(string)
            
        return string
    
    
    def to_file(self, path:str|PathLike, encoded:bool=True):
        
        with open(path, "w") as file:
            string = self.to_string(encoded=encoded)
            
            file.write(string)


    @classmethod
    def from_file(cls, path:str|PathLike, encoded:bool=True) -> Self:
        
        with open(path, "r") as file:
            
            string = file.read()
            
            return cls.from_string(string,encoded=encoded)
