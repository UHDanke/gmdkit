# Imports
from typing import Self
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
    ENCODER = staticmethod(dict_cast(PROPERTY_ENCODERS,numkey=True,default=serialize))
    DEFAULTS = OBJECT_DEFAULT
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @classmethod
    def from_string(cls, string, key_format:dict=None) -> Self:
        try:      
            return super().from_string(string.rstrip(";"))
        except:
            raise ValueError
    
    def to_string(self, key_format:dict=None) -> str:
        
        return super().to_string(encoder=key_format) + ";"

    @classmethod
    def default(cls, object_id) -> Self:
        
        return cls(cls.DEFAULTS.get(object_id,{}))


class ObjectList(ArrayDecoderMixin,ListClass):
    
    __slots__ = ()
    
    SEPARATOR = ";"
    DECODER = Object.from_string
    ENCODER = staticmethod(lambda x, **kwargs: x.to_string(**kwargs))
    
    def __init__(self, *args):
        
        super().__init__(*args)
    
    
    @classmethod
    def from_string(cls, string, encoded:bool=False, key_format:dict=None):
        
        if encoded:
            string = decode_string(string)
        
        if key_format:
            decoder = lambda string: Object.from_string(string,key_format=key_format) 
        else:
            decoder = cls.DECODER
            
        return super().from_string(string.strip(";"),decoder=decoder)


    def to_string(self, encoded:bool=False, key_format:dict=None) -> str:
                
        string = "".join([obj.to_string(key_format=key_format) for obj in self])
        
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
