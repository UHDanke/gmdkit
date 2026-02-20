# Imports
from typing import Optional, Callable
from dataclasses import dataclass, field

# Package Imports
from gmdkit.utils.typing import StringDictDecoder, StringDictEncoder
from gmdkit.serialization.functions import compile_dataclass_codec

def dataclass_decoder(
        decoder:Optional[StringDictDecoder]=None, 
        encoder: Optional[StringDictEncoder]=None, 
        separator:Optional[str]=None,
        list_format:Optional[bool]=None,
        *args, 
        **kwargs
        ):
    
    def wrap(cls):
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


def field_decoder(
        decoder:Optional[Callable]=None,
        encoder:Optional[Callable]=None,
        key:Optional[str]=None,
        allowed_kwargs=None,
        **kwargs
        ):
    
    d = kwargs
            
    if decoder is not None:
        d.setdefault("metadata",{})
        d["metadata"]["decoder"] = decoder
    
    if encoder is not None:
        d.setdefault("metadata",{})
        d["metadata"]["encoder"] = encoder

    if key is not None:
        d.setdefault("metadata",{})
        d["metadata"]["key"] = key
         
    if allowed_kwargs is not None:
        d.setdefault("metadata",{})
        d["metadata"]["kwargs"] = allowed_kwargs
         
    return field(**d)
    
    