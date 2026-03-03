# Imports
from typing import Any, Optional, Callable
from operator import attrgetter
import base64
from enum import Enum, IntEnum

# Package Imports
from gmdkit.utils.typing import NumKey


get_string = attrgetter("string")

def to_bool(string:str) -> bool:
    return string == "1"

def from_bool(obj:bool) -> str:
    return "1" if obj else "0"
    
def from_float(obj:float) -> str:
    return str(int(obj)) if obj.is_integer() else str(obj)

def to_numkey(key:str) -> NumKey:
    if key[0] == 'k':
        return key
    return int(key)

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


def serialize(obj: Any) -> str:
    t = type(obj)
    if t is str:   return obj
    if t is bool:  return from_bool(obj)
    if t is int:   return str(obj)
    if t is float: return from_float(obj)
    if obj is None: return ""
    if isinstance(obj, IntEnum): return str(obj.value)
    if isinstance(obj, Enum):    return str(obj.value)
    return to_string(obj)


def dict_serializer(key:NumKey, value:Any):
    return (str(key), serialize(value))

def dict_cast(
        functions: dict,
        allow_kwargs: Optional[set] = None,
        key_start: Optional[Callable] = None,
        key_end: Optional[Callable] = None,
        default: Optional[Callable] = None,
        ) -> Callable:
    f_get = functions.get
    has_kwargs: set = allow_kwargs or set()
    has_default: bool = callable(default)
    kc_start: bool = callable(key_start)
    kc_end: bool = callable(key_end)

    def cast_func(key: Any, value: Any) -> tuple:
        if kc_start:
            key = key_start(key)  # type: ignore[misc]
        func = f_get(key)
        if func is not None:
            value = func(value) if not has_kwargs else func(value, **{})
        elif has_default:
            value = default(value)  # type: ignore[misc]
        if kc_end:
            key = key_end(key)  # type: ignore[misc]
        return key, value

    return cast_func