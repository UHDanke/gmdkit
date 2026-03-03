# Imports
from typing import Any
from operator import attrgetter
import base64
from enum import Enum, IntEnum

# Package Imports
from gmdkit.utils.typing import NumKey


get_string = attrgetter("string")

def to_bool(string:str) -> bool:
    return bool(int(string))

def from_bool(obj:bool) -> str:
    return str(int(bool(obj)))
    
def from_float(obj:float) -> str:
    return str(int(obj)) if obj.is_integer() else str(obj)

def to_numkey(key:str) -> NumKey:
    return int(key) if key.isdigit() else key

def to_string(obj: Any, **kwargs) -> str:
    method = getattr(obj, "to_string", None)
    if method is not None:
        return method(**kwargs)
    raise TypeError(f"Object of type {type(obj).__name__} is not serializable")

def to_node(obj: Any, **kwargs):
    method = getattr(obj, "to_node", None)
    if method is not None:
        return method(**kwargs)
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
    
    t = type(obj)
    
    if t is str: return obj
    if t is float: return from_float(obj)
    if t is int: return str(obj)
    if t is bool: return from_bool(obj)
    if obj is None: return ""
    if isinstance(obj, IntEnum): return str(obj.value)
    if isinstance(obj, Enum): return str(obj.value)
    if isinstance(obj, float): return from_float(obj)
    if isinstance(obj, int): return str(obj)
    if isinstance(obj, bool): return from_bool(obj)
    
    return to_string(obj)

def dict_serializer(key:NumKey, value:Any):
    return (str(key), serialize(value))

        