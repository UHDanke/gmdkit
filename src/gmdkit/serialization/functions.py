# Imports
from typing import Callable, Literal, Optional, Any, get_type_hints
from functools import partial
from inspect import signature
from itertools import cycle
from dataclasses import field, fields, dataclass, MISSING
import sys
import xml.etree.ElementTree as ET
import base64
import zlib
import gzip

# Package Imports
from gmdkit.serialization.type_cast import (
    from_float, from_bool, to_bool
    )
from gmdkit.utils.typing import (
    StringDictDecoder, 
    StringDictEncoder,
    PathString,
    Element
    )

def xor(data: bytes, key: bytes) -> bytes:
    return bytes(d ^ k for d, k in zip(data, cycle(key)))

def decompress_string(
        string:str,
        xor_key:Optional[bytes]=None,
        compression:Optional[Literal["zlib","gzip","deflate","auto"]]="auto"
        ) -> str:
    
    byte_stream = string.encode()
    
    if xor_key is not None:
        byte_stream = xor(byte_stream, key=xor_key)
    
    byte_stream = base64.urlsafe_b64decode(byte_stream)
    
    match compression:
        case 'zlib':
            byte_stream = zlib.decompress(byte_stream, wbits=zlib.MAX_WBITS)
        case 'gzip':
            byte_stream = gzip.decompress(byte_stream)
        case 'deflate':
            byte_stream = zlib.decompress(byte_stream, wbits=-zlib.MAX_WBITS)
        case 'auto':
            byte_stream = zlib.decompress(byte_stream, wbits=zlib.MAX_WBITS|32)
        case None:
            pass            
        case _:
            raise ValueError(f"Unsupported decompression method: {compression}")

    return byte_stream.decode("utf-8",errors='replace')


def compress_string(
        string:str,
        xor_key:Optional[bytes]=None,
        compression:Optional[Literal["zlib","gzip","deflate"]]="gzip"
        ) -> str:
    
    byte_stream = string.encode()
        
    match compression:
        case 'zlib':
            byte_stream = zlib.compress(byte_stream, wbits=zlib.MAX_WBITS)
        case 'gzip':
            byte_stream = gzip.compress(byte_stream, mtime=0)
        case 'deflate':
            byte_stream = zlib.compress(byte_stream, wbits=-zlib.MAX_WBITS)
        case None:
            pass
        case _:
            raise ValueError(f"Unsupported compression method: {compression}")
            
    byte_stream = base64.urlsafe_b64encode(byte_stream)
    
    if xor_key is not None:
        byte_stream = xor(byte_stream, key=xor_key)
    
    return byte_stream.decode()


def read_plist(node:Element) -> [int,float,str,bool,dict,list]:
    
    match node.tag:
        case 'i':
            return int(node.text)
        case 'r':
            return float(node.text)
        case 's':
            return node.text or ""
        case 't':
            return True
        case 'd'|'dict':
            num = len(node)
            
            if num == 0:
                return {}
            
            if (
                    num >= 2 and
                    node[0].tag == "k" and
                    node[0].text == "_isArr" and
                    node[1].tag == "t"
                    ):
                return [read_plist(node[i]) for i in range(3, len(node), 2)]
            
            return {
                node[i].text: read_plist(node[i + 1])
                for i in range(0, len(node) - 1, 2)
            }
        case _:
            raise ValueError(f"Unknown node tag: {node.tag} for node {node}")
            

def write_plist(value:Any) -> Element:
    
    if isinstance(value, bool):
        if value: 
            return Element("t")
        
    elif isinstance(value, int):
        node = Element("i")
        node.text = str(value)
        return node
    
    elif isinstance(value, float):
        node = Element("r")
        node.text = from_float(value)
        return node
    
    elif isinstance(value, str):
        node = Element("s")
        node.text = value
        return node
    
    elif isinstance(value, dict):
        root = Element("d")
        
        for k, v in value.items():
            node = Element("k")
            node.text = str(k)
            root.append(node)
            root.append(write_plist(v))
        
        return root
    
    elif isinstance(value, (list, tuple)):
        root = Element("d")
        node = Element("k")
        node.text = "_isArr"
        root.append(node)
        root.append(Element("t"))
        
        for k, v in enumerate(value,start=1):
            node = Element("k")
            node.text = f"k_{k}"
            root.append(node)
            root.append(write_plist(v))
        
        return root
    
    else:
        raise ValueError(f"Class {type(value)} is not serializable")
    

def validate_dict_node(node:ET.Element, is_array:bool=False, encoder_key:Optional[int]=None):
    
    if node.tag not in ['d', 'dict']:
        raise ValueError("Element is not a plist dict element")
    
    length = len(node)
    
    if length % 2 != 0:
        raise ValueError(f"odd number of elements: {length}")
    
    if length < 2:
        if is_array:
            raise ValueError(f"Expected at least 2 header elements for array, found {length}")
        elif encoder_key is not None:
            raise ValueError(f"Expected at least 2 header elements for encoded struct, found {length}")
        else:
            return
        
    key_el = node[0]
    val_el = node[1]
    
    array_header = key_el.tag == 'k' and key_el.text == '_isArr' and val_el.tag == 't' and val_el.text is None
    encoder_header = key_el.tag == 'k' and key_el.text == 'kCEK' and val_el.tag == 'i' and val_el.text is not None
    
    if is_array:
        if not array_header:
            raise ValueError(f"Malformed array header, expected '<k>_isArr</k><t />', got '{ET.tostring(key_el).decode()}{ET.tostring(val_el).decode()}'")
    elif encoder_key is not None:
        if not encoder_header:
            if key_el.tag != 'k' or key_el.text != 'kCEK' or val_el.tag != 'i':
                raise ValueError(f"Malformed encoded struct header, expected '<k>kCEK</k><i>{encoder_key}</i>', got '{ET.tostring(key_el).decode()}{ET.tostring(val_el).decode()}'")
            elif node[1].text != str(encoder_key):
                raise ValueError(f"Encoder key mismatch, expected '{encoder_key}', got '{val_el.text}'")
    elif array_header:
        raise ValueError("Expected plain dict, found array header")
    elif encoder_header:
        raise ValueError("Expected plain dict, found encoded struct header")
        
    for i in range(0, length, 2):
        if node[i].tag != 'k':
            raise ValueError(f"Expected key tag 'k' at index {i}, got '{node[i].tag}'")


def from_plist_string(string: str) -> dict:
    tree = ET.fromstring(string)
    return read_plist(tree.find("dict"))


def to_plist_string(data:[dict,list]) -> str:
    root = ET.Element("plist", version="1.0", gjver="2.0")
    node = write_plist(data)
    node.tag = "dict"
    root.append(node)
    return ET.tostring(root, encoding='unicode').decode()


def from_plist_file(path: PathString) -> dict:
    tree = ET.parse(path)
    root = tree.getroot()
    return read_plist(root.find("dict"))


def to_plist_file(data: Any, path: PathString):
    root = ET.Element("plist", version="1.0", gjver="2.0")
    node = write_plist(data)
    node.tag = "dict"
    root.append(node)
    tree = ET.ElementTree(root)
    tree.write(path, xml_declaration=True)


def decoder_from_type(type_hint:Any):
    
    if type_hint is bool:
        return to_bool
    
    if callable(type_hint):
        return type_hint
 
    raise ValueError(f"Unsupported type hint: {type_hint}")
        

def encoder_from_type(type_hint:Any):
    
    if type_hint is bool:
        return from_bool
    
    if type_hint is float:
        return from_float
    
    if type_hint is int:
        return str
    
    if type_hint is str:
        return str
    
    raise ValueError(f"Unsupported type hint: {type_hint}")


def dataclass_decoder(
        cls=None,
        decoder:Optional[StringDictDecoder]=None, 
        encoder:Optional[StringDictEncoder]=None,
        condition:Optional[Callable]=None,
        separator:Optional[str]=None,
        from_array:Optional[bool]=None,
        auto_key: Optional[Callable] = None,
        default_optional: bool = False,
        default_kwargs: bool = False,
        *args,
        **kwargs
        ):
    
    def wrap(cls):        
        cls = dataclass(cls, *args, **kwargs)
        hints = get_type_hints(cls, globalns=vars(sys.modules[cls.__module__]))
        
        if separator is not None:
            cls.SEPARATOR = separator
        
        if from_array is not None:
            cls.FROM_ARRAY = from_array
        
        dkey_dict = {}
        ekey_dict = {}
        cond_dict = {}
        decoders = {}
        encoders = {}
        has_kwargs = set()
        
        for i, f in enumerate(fields(cls),start=1):
            meta = f.metadata
            name = f.name
            key = meta.get("key") 
            if key is None and auto_key is not None:
                key = auto_key(i)
                
            ft = hints[f.name]
                        
            if key is not None and name != key:
                if key in dkey_dict:
                    raise ValueError(f"Duplicate serialization key: {key!r}")
                dkey_dict[key] = name
                ekey_dict[name] = key
        
            decoders[name] = meta.get("decoder") or decoder_from_type(ft)
            encoders[name] = meta.get("encoder") or encoder_from_type(ft)
        
            
            allow_kwargs = meta.get("allow_kwargs")
            allow_kwargs = default_kwargs if allow_kwargs is None else allow_kwargs
            
            if allow_kwargs:
                has_kwargs.add(name)
            
            optional = meta.get("optional")
            optional = default_optional if optional is None else optional
            
            if optional:
                if f.default_factory is not MISSING:
                    default = f.default_factory()
                elif f.default is not MISSING:
                    default = f.default
                else:
                    default = None
                cond_dict[name] = default
                
        cls.DECODER = staticmethod(
            decoder or dict_cast(
                decoders,
                key_start=dkey_dict.get if dkey_dict else None,
                allow_kwargs=has_kwargs
                )
            )
            
        cls.ENCODER = staticmethod(
            encoder or dict_cast(
                encoders,
                key_end=ekey_dict.get if ekey_dict else None,
                allow_kwargs=has_kwargs
        		)
            )
        
        if cond_dict:
            def is_default(key, value):
                return key in cond_dict and cond_dict[key] == value
        else:
            is_default = None                
        
        cls.CONDITION = staticmethod(condition or is_default)
        
        return cls
    
    return wrap if cls is None else wrap(cls)


def field_decoder(
        *args,
        key:Optional[str]=None,
        decoder:Optional[Callable]=None,
        encoder:Optional[Callable]=None,
        optional:Optional[bool]=None,
        allow_kwargs:Optional[bool]=None,
        **kwargs
        ):
    
    d = dict(kwargs)
    
    original_md = d.get("metadata")
    if original_md is not None and not isinstance(original_md, dict):
        raise TypeError(f"'metadata' must be a dict if provided, got {type(original_md).__name__}")
    
    md = dict(original_md) if original_md else {}
            
    if "decoder" not in md and decoder is not None:
        md["decoder"] = decoder
    
    if "encoder" not in md and encoder is not None:
        md["encoder"] = encoder
        
    if "key" not in md and key is not None:
        md["key"] = key
    
    if "optional" not in md and optional is not None:
            md["optional"] = optional
        
    if "allow_kwargs" not in md and allow_kwargs is not None:
        md["allow_kwargs"] = allow_kwargs
                 
    if md:
        d["metadata"] = md
    elif "metadata" in d:
        d.pop("metadata")
        
    return field(*args, **d)


def dict_cast(
        functions: dict[Any,Callable],
        allow_kwargs: Optional[set] = None,
        key_start: Optional[Callable] = None,
        key_end: Optional[Callable] = None,
        default: Optional[Callable] = None,
        ):
    has_kwargs = allow_kwargs or set()
    f_get = functions.get
    has_default = callable(default)
    kc_start = callable(key_start)
    kc_end = callable(key_end)

    def cast_func(key: Any, value: Any, **kwargs) -> tuple[Any, Any]:
        
        if kc_start:
            key = key_start(key)
            
        func = f_get(key)

        if func is not None:
            
            value = func(value, **kwargs) if key in has_kwargs else func(value)
            
        elif has_default:
            value = default(value)

        if kc_end:
            key = key_end(key)
        

        return key, value

    return cast_func


def from_node(function:Callable):
    def get_node_text(node, **kwargs):
        return function(node.text, **kwargs)
    
    return get_node_text


def from_node_dict(functions:dict[str,Callable],exclude:Optional[dict[str,bool]]=None):
    
    d = {}
    
    for k, f in functions.items():
        if exclude and k in exclude:
            d[k] = f
        else:
            d[k] = from_node(f)
            
    return d


def to_node(function:Callable):
    def return_node(value, **kwargs):
        string = function(value, **kwargs)
        return write_plist(string)
    
    return return_node

def to_node_dict(functions:dict[str,Callable],exclude:Optional[dict[str,bool]]=None):
    
    d = {}
    
    for k, f in functions.items():
        if exclude and k in exclude:
            d[k] = f
        else:
            d[k] = to_node(f)
            
    return d
    
    
def key_node(string):
    node = ET.Element("k")
    node.text = string
    return node
        

def filter_kwargs(*functions:Callable, **kwargs) -> list[Callable]:
    """
    Filters keyword arguments to only those present on the given functions.
    
    Parameters
    ----------
    *functions : Callable
        One or more functions to retrieve the parameters from.
        
    **kwargs : dict[str,Any]
        The keyword arguments to filter.
        
    Returns
    -------
    funcs : list[Callable]
        A list containing functions with embedded kwargs.
        
    """
    if not kwargs: 
        return functions
    kw_keys = set(kwargs)
    result = []
    
    for fn in functions:
        params = signature(fn).parameters
        if params:
            kw = {k: kwargs[k] for k in kw_keys & params}
            if kw:
                result.append(partial(fn, **kw))
            else:
                result.append(fn)
        else:
            result.append(fn)
    
    return result