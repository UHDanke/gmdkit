# Imports
from typing import Callable, Any, Optional
import base64

# Package Imports
from gmdkit.serialization import options
from gmdkit.serialization.typing import NumKey


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
    

def to_string(obj:Any, **kwargs) -> str:
    method = getattr(obj, "to_string", None)
    if callable(method):
        return method(**kwargs)

    if options.string_fallback.get():
        return str(obj)

    raise TypeError(f"Object of type {type(obj).__name__} is not serializable")


def to_plist(obj:Any, **kwargs) -> str:
    method = getattr(obj, "to_plist", None)
    if callable(method):
        return method(**kwargs)

    if options.string_fallback.get():
        return str(obj)

    raise TypeError(f"Object of type {type(obj).__name__} is not serializable")


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


decode_funcs = {
    bool: to_bool
    }


encode_funcs = {
    bool: from_bool,
    float: from_float    
    }
    
    
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


def dict_cast(
    functions: dict[NumKey,Callable],
    key_kwargs: Optional[dict[NumKey,Callable]] = None,
    numkey: bool = False,
    default: Optional[Callable] = None,
):
    key_kwargs = key_kwargs or {}
    f_get = functions.get
    kw_get = key_kwargs.get
    has_default = callable(default)

    def cast_func(key: NumKey, value: Any, **kwargs) -> tuple[NumKey, Any]:
        
        if numkey and isinstance(key, str) and key.isdigit():
            key = int(key)

        func = f_get(key)

        if func is not None:
            kw_func = kw_get(key)
            if kw_func:
                kw = kw_func(**kwargs)
                value = func(value, **kw) if kw else func(value)
            else:
                value = func(value)
                
        elif has_default:
            value = default(value)

        if not numkey:
            key = str(key)

        return key, value

    return cast_func

        