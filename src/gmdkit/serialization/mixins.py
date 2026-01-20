# Imports
from dataclasses import fields
from typing import Callable, Any, Self, get_type_hints
from itertools import islice
from os import PathLike

# Package Imports
from gmdkit.serialization import options
from gmdkit.serialization.types import FilterItemsView
from gmdkit.serialization.type_cast import serialize, dict_cast, decode_funcs
from gmdkit.serialization.functions import (
    decode_string, encode_string, 
    from_plist_file, to_plist_file, 
    from_plist_string, to_plist_string,
    dict_wrapper, array_wrapper
)

class PlistDecoderMixin:
    
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
        
        return new
    
    
    @classmethod
    def from_file(cls, path:str|PathLike, **kwargs) -> Self:
        
        parsed = from_plist_file(path)
        
        new = cls.from_plist(parsed,**kwargs)
        new.path = path
                        
        return new
    
    
    def to_file(self, path:str|PathLike, **kwargs):
            
        data = self.to_plist(**kwargs)
        
        to_plist_file(data, path)
    
    def update(self, **kwargs):
        self.to_file(path=self.path, **kwargs)
    
    def reload(self, **kwargs):
        self.from_file(path=self.path, **kwargs)
    
    @classmethod
    def from_string(cls, string:str, **kwargs):
        
        parsed = from_plist_string(string)
        
        return cls.from_plist(parsed, **kwargs)
    
    
    def to_string(self, **kwargs):
        
        data = self.to_plist(self, **kwargs)
        
        return to_plist_string(data)


class PlistDictDecoderMixin(PlistDecoderMixin):
    
    __slots__ = ()
    
    PLIST_FORMAT = staticmethod(dict_wrapper)
    SELF_FORMAT = staticmethod(dict_wrapper)


class PlistArrayDecoderMixin(PlistDecoderMixin):
    
    __slots__ = ()
    
    PLIST_FORMAT = staticmethod(array_wrapper)
    SELF_FORMAT = staticmethod(array_wrapper)
    
    
class DataclassDecoderMixin:
    
    __slots__ = ()
    
    SEPARATOR = ','
    LIST_FORMAT = True
    ENCODER = staticmethod(lambda key, value: (key,serialize(value)))
    DECODER = None
    
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
    
        if cls.DECODER is None:
            type_hints = get_type_hints(cls)
            
            for k, v in type_hints.items():
                type_hints[k] = decode_funcs.get(v,v)
    
            cls.DECODER = staticmethod(dict_cast(type_hints))
        
        
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
        
            key, value = decoder(key,value)    
            
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
        
        separator = separator if separator is not None else cls.SEPARATOR
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
                
                key, value = decoder(token,value)
                    
                if not hasattr(cls, key): continue
                
                class_args[key] = value
                    
        return cls(**class_args)
    
    
    def to_string(
            self, 
            separator:str=None, 
            list_format:bool=None, 
            encoder:Callable[[str,Any],str]=None
            ) -> str:
        
        separator = separator if separator is not None else self.SEPARATOR
        list_format = list_format or self.LIST_FORMAT
        encoder = encoder or self.ENCODER
        
        parts = []
        
        for field in fields(self):
            
            key = field.name
            value = getattr(self, key, None)
            
            key, value = encoder(field.name, getattr(self,key))
            
            if list_format:
                string = value
            else:
                string = separator.join((key,value))
            
            parts.append(string)
            
        return separator.join(parts)
       
    
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
            decoder:Callable[[int|str,Any],Any]=None,
            condition:Callable=None
            ) -> Self:
        
        separator = separator if separator is not None else cls.SEPARATOR
        decoder = decoder or cls.DECODER or (lambda key, value: (key, value))
        use_condition = callable(condition)

        tokens = string.split(separator)
        if len(tokens) % 2 != 0:
            raise ValueError("Malformed input string: uneven key/value pairs")

        result = cls()
        for raw_key, raw_value in zip(tokens[::2], tokens[1::2]):
            key, value = decoder(raw_key, raw_value)
            if not use_condition or condition(key, value):
                result[key] = value

        return result
    
    
    def to_string(
            self, 
            separator:str=None, 
            encoder:Callable[[int|str,Any],str]=None,
            condition:Callable=None
            ) -> str:
        separator = separator or self.SEPARATOR
        encoder = encoder or self.ENCODER
        
        use_condition = callable(condition)

        parts: list[str] = []
        for key, value in self.items():
            if not use_condition or condition(key, value):
                parts.extend(encoder(key, value))
        
        return separator.join(parts)

class ArrayDecoderMixin:
    
    __slots__ = ()
    
    SEPARATOR = ','
    END_SEP = False
    GROUP_SIZE = 1
    ENCODER = staticmethod(serialize)
    DECODER = None
    
    @classmethod
    def from_string(
            cls, 
            string:str, 
            separator:str=None,
            end_sep:bool=None,
            group_size:int=None, 
            decoder:Callable[[str],Any]=None
            ) -> Self:
        
        separator = separator if separator is not None else cls.SEPARATOR
        end_sep = end_sep or cls.END_SEP
        group_size = group_size or cls.GROUP_SIZE
        decoder = decoder or cls.DECODER or (lambda x: x)
        
        result = cls()
        
        if string == '': return result
        
        tokens = iter(string.split(separator))
        
        while True:
            if group_size > 1:
                item = [i+separator if end_sep else i for i in islice(tokens, group_size)]
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
            end_sep:bool=None,
            encoder:Callable[[Any],str]=None
            ) -> str:
        
        end_sep = end_sep or self.END_SEP
        separator = '' if end_sep else separator if separator is not None else self.SEPARATOR
        encoder = encoder or self.ENCODER or str

        return separator.join([encoder(x) for x in self])
    

class DictDefaultMixin:
    
    KEY_DEFAULTS = None
    
    def get_keydef(self, key:int|str):
        if not self.KEY_DEFAULTS: return 
        return self.KEY_DEFAULTS.get(key, None)
    
    def auto_keydef(self, *args):
        for k in args:
            if k not in self and (v:=self.get_keydef(k)) is not None:
                self[k] = v
    
    def reset_keydef(self, *args):
        for k in args:
            if (v:=self.get_keydef(k)) is not None:
                self[k] = v
                
    def to_string(self, skip_default:bool=False, condition:Callable|None=None,**kwargs):
        
        get_default = self.KEY_DEFAULTS and (skip_default or options.discard_default.get())
        use_condition = callable(condition)
        
        if get_default and use_condition:
            func = lambda k,v: condition(k,v) and v != self.get_keydef(k)
        elif get_default:
            func = lambda k,v: v != self.get_keydef(k)
        elif use_condition:
            func = condition
        else:
            func = None
        
        return super().to_string(condition=func)


class DelimiterMixin:
    
    START_DELIMITER = None
    END_DELIMITER = None
    
    @classmethod
    def from_string(
            cls,
            string:str,
            *args,
            start_delimiter:str=None,
            end_delimiter:str=None,
            **kwargs
            ) -> Self:
        
        start_delimiter = start_delimiter or cls.START_DELIMITER
        end_delimiter = end_delimiter or cls.END_DELIMITER
        
        if start_delimiter: string = string.lstrip(start_delimiter)
        if end_delimiter: string = string.rstrip(end_delimiter)
        
        return super().from_string(string, *args, **kwargs)
    
    
    def to_string(
            self,
            *args,
            start_delimiter:str=None,
            end_delimiter:str=None,
            **kwargs
            ) -> Self:
        
        start_delimiter = start_delimiter or self.START_DELIMITER
        end_delimiter = end_delimiter or self.END_DELIMITER
        
        string = super().to_string(*args, **kwargs)
        if string:
            if start_delimiter: string = start_delimiter + string
            if end_delimiter: string = string + end_delimiter
        
        return string


class LoadFileMixin:
    
    DEFAULT_PATH = None
    COMPRESSION = None
    CYPHER = None
    
    @classmethod
    def from_file(
            cls, 
            path:str|PathLike=None, 
            encoded:bool=True, 
            compression:str=None, 
            cypher:bytes=None,
            **kwargs
            ) -> Self:
        
        path = path or cls.DEFAULT_PATH
        compression = compression or cls.COMPRESSION
        cypher = cypher or cls.CYPHER
        
        with open(path, "r", encoding="utf-8") as file:
            
            string = file.read()
            
            if encoded: string = decode_string(string, compression=compression, xor_key=cypher)
            
            return super().from_string(string, **kwargs)
        
    
    def to_file(
            self,
            path:str|PathLike=None,
            compression:str=None, 
            cypher:bytes=None,
            encoded:bool=True, 
            **kwargs
            ):
        
        path = path or self.DEFAULT_PATH
        compression = compression or self.COMPRESSION
        cypher = cypher or self.CYPHER
        
        with open(path, "w", encoding="utf-8") as file:
            
            string = super().to_string(**kwargs)
            
            if encoded: string = encode_string(string, compression=compression, xor_key=cypher)
            
            file.write(string)
