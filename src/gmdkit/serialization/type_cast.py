# Imports
from typing import Callable, Any
import base64

# Package Imports
from gmdkit.serialization import options
from gmdkit.utils.typing import NumKey


def to_bool(string:str) -> bool:
    return bool(int(string))


def from_bool(obj:bool) -> str:
    return str(int(bool(obj)))
    
    
def from_float(obj:float) -> str:
    decimals = options.float_precision.get()
    if decimals is None:
        if obj.is_integer():
            return str(int(obj))
        else:
            return str(obj)
    else:
        return f"{obj:.{decimals}f}".rstrip('0').rstrip('.')

def to_float_from_int(string:str, scale=0) -> str:
    return int(string) / 10**scale

def from_float_to_int(obj:float, scale=0) -> str:
    return str(int(obj * 10**scale))


def args_to_int(*args):
    return (int(a) for a in args)

def args_to_str(*args):
    return (str(a) for a in args)

def to_string(obj:Any, **kwargs) -> str:
    if obj is None:
        return ""
    method = getattr(obj, "to_string", None)
    if callable(method):
        return method(**kwargs)

    if options.string_fallback.get():
        return str(obj)

    raise TypeError(f"Object of type {type(obj).__name__} is not serializable")


def to_numkey(key:str) -> NumKey:
    if key.isdigit():
        key = int(key)
    return key

def to_node(obj:Any, **kwargs) -> str:
    method = getattr(obj, "to_node", None)
    if callable(method):
        return method(**kwargs)

    if options.string_fallback.get():
        return str(obj)

    raise TypeError(f"Object of type {type(obj).__name__} is not serializable")


def from_optional(method:Callable):
    
    def from_string(string:str):
        if string == "":
            return None
        else:
            return method(string)
        
    return from_string


def to_optional(method:Callable):
    
    def to_string(obj:Any):
        if obj is None:
            return ""
        else:
            return method(obj)
        
    return to_string
    
    
def zip_string(obj:Any) -> str:
    
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

    
def serialize(obj:Any) -> str:
    
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


def dict_serializer(key:NumKey, value:Any):
    return (str(key), serialize(value))

        