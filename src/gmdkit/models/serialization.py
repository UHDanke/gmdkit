# Imports
from dataclasses import fields, dataclass
from typing import Literal, Callable
from itertools import islice
from typing import get_type_hints, Callable, Any, Self
from pathlib import Path
from os import PathLike
import xml.etree.ElementTree as ET
import base64
import zlib
import gzip


def serialize(value:Any) -> str:
    
    if value is None:
        return ''
        
    elif isinstance(value, bool):
        return str(int(value))
    
    elif isinstance(value, float):           
        return str(value)
    
    else:
        return str(value)


def decode_string(string:str) -> str:

    base64_decoded = base64.urlsafe_b64decode(string.encode())
    
    decompressed = gzip.decompress(base64_decoded)
        
    return decompressed.decode()


def encode_string(string:str) -> str:
    
    gzipped = gzip.compress(string.encode(),mtime=0)
        
    base64_encoded = base64.urlsafe_b64encode(gzipped)
    
    return base64_encoded.decode()


def xor(string: str, key: int) -> str:
    
    return ("").join(chr(ord(char) ^ key) for char in string)


def decode_save(data: str) -> str:

    return decode_string(xor(data, key=11))


def encode_save(data: str) -> str:

    return xor(encode_string(data), key=11)


def read_plist_elem(elem):
        
    match elem.tag:
        case 'i':
            return int(elem.text)
        case 'r':
            return float(elem.text)
        case 's':
            return str(elem.text)
        case 't':
            return True
        case 'd':
            return read_plist(elem)
        
        
def read_plist(node):
    
    nodes = len(node)
        
    if nodes == 0:
        return None
      
    if (    
            nodes > 0 and
            node[0].tag == "k" and node[0].text == "_isArr" and
            read_plist_elem(node[1])
            ):
        result = []
        
        for child in islice(node, 2, None):
            match child.tag:
                case 'k':
                    continue
                case _:
                    result.append(read_plist_elem(child))
        
    else:
        result = {}
        key = None
        
        for child in node:
            match child.tag:
                case 'k':
                    key = child.text
                    continue
                case _:
                    value = read_plist_elem(child)
                    if key is not None:
                        result[key] = value
                        
                        key = None
    
    return result


def write_plist_elem(parent, value):
    
    if isinstance(value, bool) and value:
        ET.SubElement(parent, "t")
        
    elif isinstance(value, int):
        ET.SubElement(parent, "i").text = str(value)
    
    elif isinstance(value, float):
        ET.SubElement(parent, "r").text = str(value)
    
    elif isinstance(value, str):
        ET.SubElement(parent, "s").text = str(value)
    
    elif isinstance(value, (dict, list, tuple)):
        write_plist(ET.SubElement(parent, "d"),value)
    
    elif value is None:
        pass
    
    else:
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
            
    
def from_plist_string(string:str):
    
    tree = ET.fromstring(string)
    
    return read_plist(tree.find("dict"))
    

def to_plist_string(data:dict|list|tuple) -> str:
    
    root = ET.Element("plist", version="1.0", gjver="2.0")
    
    dict_elem = ET.SubElement(root, "dict")
    
    write_xml(dict_elem, data)
    
    return ET.tostring(root, encoding='unicode') 


def from_plist_file(path:str|PathLike):
    
    tree = ET.parse(path)
    
    root = tree.getroot()
    
    parsed_xml = read_plist(root.find("dict"))
        
    return parsed_xml


def to_plist_file(data:dict|list|tuple, path:str|PathLike):
    
    #print(data)
    root = ET.Element("plist", version="1.0", gjver="2.0")
   
    dict_elem = ET.SubElement(root, "dict")
    
    write_plist(dict_elem, data)
           
    tree = ET.ElementTree(root)
    
    tree.write(path, xml_declaration=True)


def dict_cast(dictionary:dict, numkey:bool=False, default:Callable=None, key_kwargs:bool=False):
    
    def cast_func(key:str, value:Any, **kwargs):
        
        if numkey and key.isdigit():
            key = int(key)
        
        if (func:=dictionary.get(key)) is not None and callable(func):
            
            if key_kwargs: kwargs = kwargs.get(key, {})
                
            value = func(value, **kwargs)
            
        elif default is not None and callable(default):
            value = default(value)
        
        return (key,value)
            
    return cast_func


class PlistDecoderMixin:
    
    __slots__ = ()
    
    ENCODER = None
    DECODER = None
    PLIST_FORMAT = None
    SELF_FORMAT = None
    
    
    @classmethod
    def from_plist(
            cls, 
            data:Any, 
            decoder:Callable=None,
            self_format:Callable[Any,Callable]=None, 
            fkwargs:dict=None,
            **kwargs
            ) -> Self:
        
        decoder = decoder or cls.DECODER
        self_format = self_format or cls.SELF_FORMAT
        fkwargs = fkwargs or {}
        
        if decoder is None or not callable(decoder) or self_format is None or not callable(self_format):
            return cls(data, **kwargs)
        
        new = self_format(data, decoder, **fkwargs)
        
        return cls(new, **kwargs)
    
        
    def to_plist(
            self, 
            encoder:Callable=None, 
            plist_format:Callable=None,
            fkwargs:dict=None
            ) -> Any:
        
        encoder = encoder or self.ENCODER or (lambda x: x)
        plist_format = plist_format or self.PLIST_FORMAT
        fkwargs = fkwargs or {}
        
        if encoder is None or not callable(encoder) or plist_format is None or not callable(plist_format):
            return self
        
        new = plist_format(self, encoder, **fkwargs)
        #print(new)
        
        return new
    
    
    @classmethod
    def from_file(cls, path:str|PathLike, **kwargs) -> Self:
        
        parsed = from_plist_file(path)
                        
        return cls.from_plist(parsed,**kwargs)
    
    
    def to_file(self, path:str|PathLike, **kwargs):
            
        data = self.to_plist(**kwargs)
        
        to_plist_file(data, path)
    
    
    @classmethod
    def from_string(cls, string:str, **kwargs):
        
        parsed = from_plist_string(string)
        
        return cls.from_plist(parsed, **kwargs)
    
    
    def to_string(self, **kwargs):
        
        data = self.to_plist(self, **kwargs)
        
        return to_plist_string(data)


dict_formatter = lambda data, func, **kwargs: {k: v for k, v in (func(k, v, **kwargs) for k, v in data.items())}

class PlistDictDecoderMixin(PlistDecoderMixin):
    
    __slots__ = ()
    
    PLIST_FORMAT = staticmethod(dict_formatter)
    SELF_FORMAT = staticmethod(dict_formatter)


list_formatter = lambda data, func, **kwargs: [func(v,**kwargs) for v in data]

class PlistArrayDecoderMixin(PlistDecoderMixin):
    
    __slots__ = ()
    
    PLIST_FORMAT = staticmethod(list_formatter)
    SELF_FORMAT = staticmethod(list_formatter)
    

class DataclassDecoderMixin:
    
    __slots__ = ()
    
    SEPARATOR = ','
    LIST_FORMAT = True
    ENCODER = staticmethod(lambda key, value: (key,serialize(value)))
    DECODER = None
    
    @classmethod
    def from_args(cls, *args, **kwargs):
        
        decoder = cls.DECODER or dict_cast(get_type_hints(cls))
            
        class_args = dict()
        
        iarg = iter(args)
        
        for f in fields(cls):
            try:
                key, value = decoder(f.name,next(iarg))
                    
                class_args[key] = value
                
            except StopIteration:
                break
        
        for key, value in kwargs.items():
                
                if not hasattr(cls, key): continue
                
                class_args[key] = value
        
        return cls(**class_args)
    
        
    @classmethod
    def from_string(
            cls, 
            string:str, 
            separator:str=None, 
            list_format:bool=None, 
            decoder:Callable[[int|str,Any],Any]=None
            ) -> Self:
        
        separator = separator or cls.SEPARATOR
        list_format = list_format or cls.LIST_FORMAT
        decoder = decoder or cls.DECODER or dict_cast(get_type_hints(cls))
        
        if string == '':
            return cls()
            
        tokens = iter(string.split(separator))
        
        class_args = dict()
        
        if list_format:
            
            for f in fields(cls):
                try:
                    key, value = decoder(f.name,next(tokens))
                    
                    class_args[key] = value
                
                except StopIteration:
                    break
                
        else:
            
            for token in tokens:
                
                value = next(tokens)
                key, _ = decoder(token,value)
                
                if not hasattr(cls, key): continue
                
                class_args[key] = value
                    
        return cls(**class_args)
    
    
    def to_string(
            self, 
            separator:str=None, 
            dict_format:bool=None, 
            encoder:Callable[[str,Any],str]=None
            ) -> str:
        
        separator = separator or self.SEPARATOR
        dict_format = dict_format or self.DICT_FORMAT
        encoder = encoder or self.ENCODER
        
        parts = []
        
        for field in fields(self):
            
            key = field.name
            value = getattr(self, key, None)
            
            key, value = encoder(field.name, gettattr(self,key))
            
            if dict_format:
                string = separator.join((key,value))
            else:
                string = value
            
            parts.append(string)
            
        return separator.join(parts)

import inspect

class DictDecoderMixin:

    __slots__ = ()
    
    SEPARATOR = ','
    ENCODER = staticmethod(lambda key, value: (str(key),serialize(value)))
    DECODER = None
    
    @classmethod
    def from_string(
            cls, 
            string:str, 
            separator:str=None, 
            decoder:Callable[[int|str,Any],Any]=None
            ) -> Self:
        
        separator = separator or cls.SEPARATOR
        decoder = decoder or cls.DECODER or (lambda key, value: (key, value))
        
        result = cls()
        tokens = iter(string.split(separator))
    
        for token in tokens:
            key, value = decoder(token, next(tokens))
            result[key] = value
                
        return result
    
    
    def to_string(
            self, 
            separator:str=None, 
            encoder:Callable[[int|str,Any],str]=None
            ) -> str:
        
        separator = separator or self.SEPARATOR
        encoder = encoder or self.ENCODER
            
        return separator.join([separator.join(encoder(k,v)) for k,v in self.items()])
    

class ArrayDecoderMixin:
    
    __slots__ = ()
    
    SEPARATOR = ','
    GROUP_SIZE = 1
    ENCODER = staticmethod(serialize)
    DECODER = None
        
    @classmethod
    def from_string(
            cls, 
            string:str, 
            separator:str=None, 
            group_size:int=None, 
            decoder:Callable[[str],Any]=None
            ) -> Self:
        
        separator = separator or cls.SEPARATOR
        group_size = group_size or cls.GROUP_SIZE
        decoder = decoder or cls.DECODER or (lambda x: x)
        
        result = cls()
        
        if string == '':
            return result
        
        tokens = iter(string.split(separator))
        
        while True:
            if group_size > 1:
                item = list(islice(tokens, group_size))
            else:
                try:
                    item = next(tokens)
                except StopIteration:
                    break
                
            if not item:
                break
            else:
                result.append(decoder(item))
                
        return result
        
        
    def to_string(
            self, 
            separator:str=None, 
            encoder:Callable[[Any],str]=None
            ) -> str:
        
        separator = separator or self.SEPARATOR
        encoder = encoder or self.ENCODER or str
        
        return separator.join([encoder(x) for x in self])