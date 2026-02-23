# Imports
from typing import Callable, Literal, Optional, Iterable, Any, get_type_hints
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
    from_float, from_bool, to_bool,
    dict_cast, 
    )
from gmdkit.utils.typing import (
    StringDictDecoder, 
    StringDictEncoder,
    KeyValueFormat,
    PathString
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


def read_plist(node:ET.Element):
    
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


def write_plist(parent:ET.Element, value:Any):
    
    if isinstance(value, bool):
        if value: ET.SubElement(parent, "t")
        
    elif isinstance(value, int):
        ET.SubElement(parent, "i").text = str(value)
    
    elif isinstance(value, float):
        ET.SubElement(parent, "r").text = from_float(value)
    
    elif isinstance(value, str):
        ET.SubElement(parent, "s").text = str(value)

    elif isinstance(value, dict):
        if parent.tag == "plist":
            node = ET.SubElement(parent, "dict")
        else:
            node = ET.SubElement(parent, "d")
        
        for k, v in value.items():
            
            ET.SubElement(node, "k").text = k
            
            write_plist(node, v)
    
    elif isinstance(value, (list, tuple, set)):
        if parent.tag == "plist":
            node = ET.SubElement(parent, "dict")
        else:
            node = ET.SubElement(parent, "d")
        
        ET.SubElement(node, "k").text = "_isArr"
        
        ET.SubElement(node, "t")
        
        for i, v in enumerate(value,start=1):
            
            ET.SubElement(node, "k").text = f"k_{i}"
            
            write_plist(node, v)
    
    elif value is not None:
        ET.SubElement(parent, "s").text = str(value)           



def from_plist_string(string: str) -> dict:
    tree = ET.fromstring(string)
    return read_plist(tree.find("dict"))


def to_plist_string(data: Any) -> str:
    root = ET.Element("plist", version="1.0", gjver="2.0")
    write_plist(root, data)
    return ET.tostring(root, encoding='unicode')


def from_plist_file(path: PathString) -> dict:
    tree = ET.parse(path)
    root = tree.getroot()
    return read_plist(root.find("dict"))


def to_plist_file(data: Any, path: PathString):
    root = ET.Element("plist", version="1.0", gjver="2.0")
    write_plist(root, data)
    tree = ET.ElementTree(root)
    tree.write(path, xml_declaration=True)


def dict_wrapper(data:dict|ET.Element, func:Callable, **kwargs) -> dict:
    return dict(func(k, v, **kwargs) for k, v in data.items())


def array_wrapper(data:Iterable, func:Callable, **kwargs) -> list:
    return list(func(v,**kwargs) for v in data)


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
        default_optional: bool = False,
        auto_key: Optional[KeyValueFormat] = None,
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
        kw_dict = {}
        
        for i, f in enumerate(fields(cls)):
            meta = f.metadata
            name = f.name
            key = meta.get("key") 
            if key is None and auto_key is not None:
                key = auto_key(name, i)
                
            ft = hints[f.name]
                        
            if key is not None and name != key:
                if key in dkey_dict:
                    raise ValueError(f"Duplicate serialization key: {key!r}")
                dkey_dict[key] = name
                ekey_dict[name] = key
        
            decoders[name] = meta.get("decoder") or decoder_from_type(ft)
            encoders[name] = meta.get("encoder") or encoder_from_type(ft)
        
            kw = meta.get("allowed_kwargs")
            if kw:
                kw_dict[name] = kw
            
            if meta.get("optional") or default_optional:
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
                key_func_start=dkey_dict.get if dkey_dict else None,
                allowed_kwargs=kw_dict if kw_dict else None
                )
            )
            
        cls.ENCODER = staticmethod(
            encoder or dict_cast(
                encoders,
                key_func_end=ekey_dict.get if ekey_dict else None,
                allowed_kwargs=kw_dict if kw_dict else None
        		)
            )
        
        if cond_dict:
            def is_default(key, value):
                return key in cond_dict and cond_dict[key] == value
        else:
            is_default = None                
        
        cls.CONDITION = condition or is_default
        
        return cls
    
    return wrap if cls is None else wrap(cls)


def field_decoder(
        *args,
        key:Optional[str]=None,
        decoder:Optional[Callable]=None,
        encoder:Optional[Callable]=None,
        optional:Optional[bool]=None,
        allowed_kwargs=None,
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
        
    if "allowed_kwargs" not in md and allowed_kwargs is not None:
        md["allowed_kwargs"] = allowed_kwargs
                 
    if md:
        d["metadata"] = md
    elif "metadata" in d:
        d.pop("metadata")

    return field(*args, **d)


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
            result.append(partial(fn, **kw))
        else:
            result.append(fn)
    
    return result