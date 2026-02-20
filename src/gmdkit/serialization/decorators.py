# Imports
from typing import Optional, Callable
from dataclasses import dataclass, field

# Package Imports
from gmdkit.utils.typing import StringDictDecoder, StringDictEncoder
from gmdkit.serialization.type_cast import dict_cast


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
        
        if decoder:
            cls.DECODER = decoder
        else:
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
            
                decoder = meta.get("decoder")
                
                if decoder is None:
                    decoder = decode_funcs.get(ft, ft)
                
                decoders[name] = decoder
                
                encoder = meta.get("encoder")
                
                if encoder is None:
                    encoder = encode_funcs.get(ft, ft)
        
                encoders[name] = encoder
                
                kw = meta.get("kwargs")
                
                if kw:
                    kw_dict[name] = kw
                    
            
            if dkey_dict:
                dkey_get = dkey_dict.get
                dkey_func = lambda key: dkey_get(key, key)
            
            else:
                dkey_func = None
                
            if ekey_dict:
                ekey_get = ekey_dict.get
                ekey_func = lambda key: ekey_get(key, key)
            
            else:
                ekey_func = None
            
            if not kw_dict: 
                kw_dict = None
        
            cls.DECODER = staticmethod(dict_cast(
                decoders,
                key_func_start=dkey_func,
                allowed_kwargs=kw_dict
                ))
            
            cls.ENCODER = staticmethod(dict_cast(
                decoders,
                key_func_end=ekey_func,
                allowed_kwargs=kw_dict
        		))

        
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
    
    