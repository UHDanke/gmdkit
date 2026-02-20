# Imports
from typing import Optional, Callable
from dataclasses import dataclass, field, fields

# Package Imports
from gmdkit.utils.typing import StringDictDecoder, StringDictEncoder
from gmdkit.serialization.type_cast import (
    dict_cast,
    decode_funcs,
    encode_funcs
    )


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
        
        dkey_dict = {}
        ekey_dict = {}
        decoders = {}
        encoders = {}
        kw_dict = {}
        
        for f in fields(cls):
            meta = f.metadata
            name = f.name
            key = meta.get("key")
            ft = f.type
        
            if key is not None and name != key:
                dkey_dict[key] = name
                ekey_dict[name] = key
        
            decoders[name] = meta.get("decoder") or decode_funcs.get(ft, ft)
            encoders[name] = meta.get("encoder") or encode_funcs.get(ft, str)
        
            kw = meta.get("kwargs")
            if kw:
                kw_dict[name] = kw
        
        cls.DECODER = staticmethod(
            decoder or dict_cast(
                decoders,
                key_func_start=dkey_dict.get if dkey_dict else None,
                allowed_kwargs=kw_dict
                )
            )
            
        cls.ENCODER = staticmethod(
            encoder or dict_cast(
                encoders,
                key_func_end=ekey_dict.get if ekey_dict else None,
                allowed_kwargs=kw_dict
        		)
            )

        
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
    
    