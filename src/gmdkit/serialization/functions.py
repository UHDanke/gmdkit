# Imports
from typing import Callable, Literal, Optional, Iterable, Any
from functools import partial
from inspect import signature
from itertools import cycle
from os import PathLike
import xml.etree.ElementTree as ET
import base64
import zlib
import gzip

# Package Imports
from gmdkit.serialization.type_cast import from_float


def xor(data: bytes, key: bytes) -> bytes:
    return bytes(d ^ k for d, k in zip(data, cycle(key)))

def decode_string(
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


def encode_string(
        string:str,
        xor_key:Optional[bytes]=None,
        compression:Optional[Literal["zlib","gzip","deflate"]]="gzip"
        ) -> str:
    
    byte_stream = string.encode()
        
    match compression:
        case 'zlib':
            byte_stream = zlib.decompress(byte_stream, wbits=zlib.MAX_WBITS)
        case 'gzip':
            byte_stream = gzip.compress(byte_stream, mtime=0)
        case 'deflate':
            byte_stream = zlib.decompress(byte_stream, wbits=-zlib.MAX_WBITS)
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


def from_plist_file(path: str | PathLike) -> dict:
    tree = ET.parse(path)
    root = tree.getroot()
    return read_plist(root.find("dict"))

def to_plist_file(data: Any, path: str | PathLike):
    root = ET.Element("plist", version="1.0", gjver="2.0")
    write_plist(root, data)
    tree = ET.ElementTree(root)
    tree.write(path, xml_declaration=True)



def dict_wrapper(data:dict|ET.Element, func:Callable, **kwargs) -> dict:
    return dict(func(k, v, **kwargs) for k, v in data.items())


def array_wrapper(data:Iterable, func:Callable, **kwargs) -> list:
    return list(func(v,**kwargs) for v in data)


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