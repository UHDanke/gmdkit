# Imports
from typing import Optional
from dataclasses import dataclass

# Package Imports
from gmdkit.serialization.functions import compile_dataclass_codec
from gmdkit.serialization.mixins import DataclassDecoderMixin
from gmdkit.serialization.typing import StringDictDecoder, StringDictEncoder

def dataclass_decoder(
        decoder:Optional[StringDictDecoder]=None, 
        encoder: Optional[StringDictEncoder]=None, 
        separator:Optional[str]=None,
        list_format:Optional[bool]=None,
        *args, 
        **kwargs
        ):
    
    def wrap(cls):
        cls = type(cls.__name__, (cls, DataclassDecoderMixin), {})
        cls = dataclass(cls, *args, **kwargs)
        
        if not decoder and not encoder:
            compile_dataclass_codec(cls)
        
        if decoder:
            cls.DECODER = decoder
        
        if encoder:
            cls.ENCODER = encoder
        
        if separator:
            cls.SEPARATOR = separator
        
        if list_format:
            cls.LIST_FORMAT = list_format
        
        return cls
    
    return wrap if args or kwargs else wrap(args[0]) if args else wrap
