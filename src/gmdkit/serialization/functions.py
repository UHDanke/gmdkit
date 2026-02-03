# Imports
from typing import Callable, Literal
from functools import partial
from inspect import signature
from os import PathLike
import xml.etree.ElementTree as ET
import base64
import zlib
import gzip

# Package Imports
from gmdkit.serialization.type_cast import from_float


def xor(data:bytes, key:bytes) -> bytes:
    l = len(key)
    return bytes(data[i] ^ key[i % l] for i in range(len(data)))


def decode_string(
        string:str,
        xor_key:bytes|None=None,
        compression:Literal[None,"zlib","gzip","deflate","auto"]="auto"
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
        xor_key:bytes|None=None,
        compression:Literal[None,"zlib","gzip","deflate"]="gzip"
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


def read_plist_elem(elem):
        
    match elem.tag:
        case 'i':
            return int(elem.text)
        case 'r':
            return float(elem.text)
        case 's':
            return elem.text or ""
        case 't':
            return True
        case 'd':
            return read_plist(elem)
        
        
def read_plist(node):
    children = node[:]
    num_children = len(children)
    
    if num_children == 0:
        return {}
    
    if (
            num_children >= 2 and 
            children[0].tag == "k" and 
            children[0].text == "_isArr" and
            read_plist_elem(children[1])
            ):
        result = []
        for i in range(2, num_children):
            if children[i].tag != 'k':
                result.append(read_plist_elem(children[i]))
        return result
    
    result = {}
    i = 0
    while i < num_children:
        if children[i].tag == 'k':
            key = children[i].text
            if i + 1 < num_children and children[i + 1].tag != 'k':
                result[key] = read_plist_elem(children[i + 1])
                i += 2
            else:
                i += 1
        else:
            i += 1
    
    return result


def write_plist_elem(parent, value):
    
    if isinstance(value, bool):
        if value: ET.SubElement(parent, "t")
        
    elif isinstance(value, int):
        ET.SubElement(parent, "i").text = str(value)
    
    elif isinstance(value, float):
        ET.SubElement(parent, "r").text = from_float(value)
    
    elif isinstance(value, str):
        ET.SubElement(parent, "s").text = str(value)
    
    elif isinstance(value, (dict, list, tuple)):
        write_plist(ET.SubElement(parent, "d"),value)
    
    elif value is not None:
        ET.SubElement(parent, "s").text = str(value)


def write_plist(node, obj):
    
    if isinstance(obj, dict):
        
        for key, value in obj.items():
            
            ET.SubElement(node, "k").text = key
            
            write_plist_elem(node, value)
            
    elif isinstance(obj, (list,tuple)):
        
        ET.SubElement(node, "k").text = "_IsArr"
        
        ET.SubElement(node, "t")
        
        for i, value in enumerate(obj,start=1):
            
            ET.SubElement(node, "k").text = f"k_{i}"
            
            write_plist_elem(node, value)
    
    else:
        write_plist_elem(node, obj)
            
    
def from_plist_string(string:str):
    
    tree = ET.fromstring(string)
    
    return read_plist(tree.find("dict"))
    

def to_plist_string(data:dict|list|tuple) -> str:
    
    root = ET.Element("plist", version="1.0", gjver="2.0")
    
    dict_elem = ET.SubElement(root, "dict")
    
    write_plist(dict_elem, data)
    
    return ET.tostring(root, encoding='unicode') 


def from_plist_file(path:str|PathLike):
    
    tree = ET.parse(path)
    
    root = tree.getroot()
    
    parsed_xml = read_plist(root.find("dict"))
        
    return parsed_xml


def to_plist_file(data:dict|list|tuple, path:str|PathLike):
    
    root = ET.Element("plist", version="1.0", gjver="2.0")
   
    dict_elem = ET.SubElement(root, "dict")
    
    write_plist(dict_elem, data)
           
    tree = ET.ElementTree(root)
    
    tree.write(path, xml_declaration=True)


def dict_wrapper(data, function, **kwargs):
    
    return {k: v for k, v in (function(k, v, **kwargs) for k, v in data.items())}


def array_wrapper(data, function, **kwargs):
    
    return [function(v,**kwargs) for v in data]


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