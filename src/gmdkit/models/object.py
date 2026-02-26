# Imports
from typing import Self

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.serialization.mixins import (
    DictDecoderMixin, 
    ArrayDecoderMixin, 
    DelimiterMixin,
    CompressFileMixin
    )
from gmdkit.serialization.type_cast import serialize, to_string, to_numkey
from gmdkit.serialization.functions import dict_cast
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