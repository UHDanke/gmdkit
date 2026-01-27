# Imports
from typing import Callable, Any
import base64

# Package Imports
from gmdkit.serialization import options


def to_bool(string:str) -> bool:
    return bool(int(string))


def from_bool(obj:bool) -> str:
    return str(int(bool(obj)))
    
    
def from_float(obj:float):
    decimals = options.float_precision.get()
    if decimals is None:
        if obj.is_integer():
            return str(int(obj))
        else:
            return str(obj)
    else:
        return f"{obj:.{decimals}f}".rstrip('0').rstrip('.')


def to_string(obj, **kwargs) -> str:
    method = getattr(obj, "to_string", None)
    if callable(method):
        return method(**kwargs)

    if options.string_fallback.get():
        return str(obj)

    raise TypeError(f"Object of type {type(obj).__name__} is not serializable")


def to_plist(obj, **kwargs) -> str:
    method = getattr(obj, "to_plist", None)
    if callable(method):
        return method(**kwargs)

    if options.string_fallback.get():
        return str(obj)

    raise TypeError(f"Object of type {type(obj).__name__} is not serializable")


def zip_string(obj) -> str:
    method = getattr(obj, "save", None)
    if callable(method):
        return method()
    
    string = getattr(obj, "string", None)
    if string is not None:
        return string
    
    if options.string_fallback.get():
        return str(obj)

    raise TypeError(f"Object of type {type(obj).__name__} is not serializable")


def decode_text(string:str) -> str:
    
    string_bytes = string.encode("utf-8")
    
    decoded_bytes = base64.urlsafe_b64decode(string_bytes)
    
    return decoded_bytes.decode("utf-8", errors="surrogateescape")


def encode_text(string:str) -> str:
    
    string_bytes = string.encode("utf-8", errors="surrogateescape")
    
    encoded_bytes = base64.urlsafe_b64encode(string_bytes)
    
    return encoded_bytes.decode("utf-8")


decode_funcs = {
    bool: to_bool
    }


encode_funcs = {
    bool: from_bool,
    float: from_float    
    }
    
    
def serialize(obj) -> str:
    
    if isinstance(obj, str):
        return obj
    
    elif obj is None:
        return str()
    
    elif isinstance(obj, bool):
        return from_bool(obj)
    
    elif isinstance(obj, float):           
        return from_float(obj)
    
    elif isinstance(obj, int):
        return str(obj)
    
    else:
        return to_string(obj)


def dict_cast(
        dictionary:dict, 
        numkey:bool=False, 
        default:Callable|None=None, 
        key_kwargs:bool=False
        ):
    
    def cast_func(key:str, value:Any, **kwargs):
        
        if numkey and isinstance(key, str) and key.isdigit():
            key = int(key)
        
        if (func:=dictionary.get(key)) is not None and callable(func):
            
            if key_kwargs: kwargs = kwargs.get(key, {})
                
            value = func(value, **kwargs)
            
        elif default is not None and callable(default):
            value = default(value)
        
        if not numkey: key = str(key)
        
        return (key,value)
            
    return cast_func
        