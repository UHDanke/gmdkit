# Imports
from dataclasses import fields
from typing import Callable, Any, Self, get_type_hints, Literal
from os import PathLike

# Package Imports
from gmdkit.serialization import options
from gmdkit.serialization.type_cast import serialize, dict_cast, decode_funcs
from gmdkit.serialization.functions import (
    decode_string, encode_string, 
    from_plist_file, to_plist_file, 
    from_plist_string, to_plist_string,
    dict_wrapper, array_wrapper
)

Decoder = Callable[[int|str, Any], tuple[str, Any]]
DecoderWithKwargs = Callable[..., tuple[str, Any]]
DictDecoder = Callable[[int|str, Any], tuple[Any, Any]]
Encoder = Callable[[int|str, Any], tuple[str, str]]
DataclassEncoder = Callable[[str, Any], tuple[str, str]]
ArrayEncoder = Callable[[Any], str]
ArrayDecoder = Callable[[Any], Any]


class PlistDecoderMixin:
    
    __slots__ = ()
    
    ENCODER: Callable | None = None
    DECODER: Callable | None = None
    PLIST_FORMAT: Callable | None = None
    SELF_FORMAT: Callable | None = None
    path: str | PathLike | None = None
    
    
    @classmethod
    def from_plist(
            cls, 
            data:Any, 
            decoder:Callable|None=None,
            self_format:Callable|None=None, 
            fkwargs:dict[str, Any]|None=None,
            **kwargs: Any
            ) -> Self:
        
        decoder = decoder or cls.DECODER
        self_format = self_format or cls.SELF_FORMAT
        
        if decoder is None or not callable(decoder) or self_format is None or not callable(self_format):
            return cls(data, **kwargs)
        
        fkwargs = fkwargs or {}
        new = self_format(data, decoder, **fkwargs)
        
        return cls(new, **kwargs)
    
        
    def to_plist(
            self, 
            encoder:Callable|None=None, 
            plist_format:Callable|None=None,
            fkwargs:dict[str, Any]|None=None
            ) -> Any:
        
        encoder = encoder or self.ENCODER or (lambda x: x)
        plist_format = plist_format or self.PLIST_FORMAT
        
        if encoder is None or not callable(encoder) or plist_format is None or not callable(plist_format):
            return self
        
        fkwargs = fkwargs or {}
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
    
   # TODO REDO 
 
   #def reload(self, **kwargs):
   #    self.from_file(path=self.path, **kwargs)
    
    @classmethod
    def from_string(cls, string:str, **kwargs):
        
        parsed = from_plist_string(string)
        
        return cls.from_plist(parsed, **kwargs)
    
    
    def to_string(self, **kwargs):
        
        data = self.to_plist(**kwargs)
        
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
    
    SEPARATOR: str = ','
    LIST_FORMAT: bool = True
    ENCODER: DataclassEncoder = staticmethod(lambda key, value: (key,serialize(value)))
    DECODER: DecoderWithKwargs | None = None
    
    
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
        class_args = {}
        
        for field, arg in zip(fields(cls), args):
            key, value = decoder(field.name, arg)
            class_args[key] = value
        
        for key, value in kwargs.items():
            if hasattr(cls, key):
                key, value = decoder(key, value)
                class_args[key] = value
        
        return cls(**class_args)
    
        
    @classmethod
    def from_string(
            cls, 
            string:str, 
            separator:str|None=None, 
            list_format:bool|None=None, 
            decoder:DecoderWithKwargs|None=None
            ) -> Self:
        
        separator = separator if separator is not None else cls.SEPARATOR
        list_format = list_format if list_format is not None else cls.LIST_FORMAT
        
        if decoder is None and cls.DECODER is not None:
            decoder = cls.DECODER
        else:
            decoder = dict_cast(get_type_hints(cls))
        
        if not string:
            return cls()
        
        tokens = string.split(separator)
        class_args = {}
        
        if list_format:
            for field, token in zip(fields(cls), tokens):
                key, value = decoder(field.name, token)
                class_args[key] = value
        else:
            if len(tokens) % 2 != 0:
                raise ValueError("Malformed string: uneven key/value pairs")
            
            for i in range(0, len(tokens), 2):
                key, value = decoder(tokens[i], tokens[i + 1])
                if hasattr(cls, key):
                    class_args[key] = value
        
        return cls(**class_args)
    
    
    def to_string(
            self, 
            separator:str|None=None, 
            list_format:bool|None=None, 
            encoder:DataclassEncoder|None=None
            ) -> str:
        
        separator = separator if separator is not None else self.SEPARATOR
        list_format = list_format or self.LIST_FORMAT
        encoder = encoder or self.ENCODER
        
        parts = []
        for field in fields(self):
            value = getattr(self, field.name)
            key, encoded_value = encoder(field.name, value)
            
            parts.append(
                encoded_value if list_format 
                else f"{key}{separator}{encoded_value}"
                )
        
        return separator.join(parts)
       
    
class DictDecoderMixin:

    __slots__ = ()
    
    SEPARATOR: str = ','
    ENCODER: Encoder = staticmethod(lambda key, value: (str(key),serialize(value)))
    DECODER: DictDecoder | None = None
    
    @classmethod
    def from_string(
            cls, 
            string:str, 
            separator:str|None=None, 
            decoder:DictDecoder|None=None,
            condition:Callable|None=None
            ) -> Self:
        
        separator = separator if separator is not None else cls.SEPARATOR
        decoder = decoder or cls.DECODER or (lambda key, value: (key, value))

        tokens = string.split(separator)
        if len(tokens) % 2 != 0:
            raise ValueError("Malformed input string: uneven key/value pairs")
        
        result = cls()
        for raw_key, raw_value in zip(tokens[::2], tokens[1::2]):
            key, value = decoder(raw_key, raw_value)
            if condition is None or condition(key, value):
                result[key] = value
        
        return result
    
    
    def to_string(
            self, 
            separator:str|None=None, 
            encoder:Encoder|None=None,
            condition:Callable|None=None
            ) -> str:
        separator = separator or self.SEPARATOR
        encoder = encoder or self.ENCODER
        
        parts = []
        for key, value in self.items():
            if condition is None or condition(key, value):
                parts.extend(encoder(key, value))
        
        return separator.join(parts)
    

class ArrayDecoderMixin:
    
    __slots__ = ()
    
    SEPARATOR: str = ','
    KEEP_SEP: bool = False
    GROUP_SIZE: int = 1
    ENCODER: ArrayEncoder = staticmethod(serialize)
    DECODER: ArrayDecoder | None = None
    
    @classmethod
    def from_string(
            cls, 
            string:str, 
            separator:str|None=None,
            keep_sep:bool|None=None,
            group_size:int|None=None, 
            decoder:ArrayDecoder|None=None
            ) -> Self:
        
        separator = separator if separator is not None else cls.SEPARATOR
        keep_sep = keep_sep or cls.KEEP_SEP
        group_size = group_size or cls.GROUP_SIZE
        decoder = decoder or cls.DECODER

        result = cls()

        string = string.removeprefix(separator).removesuffix(separator)
        
        if not string:
            return result

        tokens = string.split(separator)
        
        if group_size > 1:
            if keep_sep:
                for i in range(0, len(tokens), group_size):
                    group = [token + separator for token in tokens[i:i + group_size]]
                    if group:
                        result.append(decoder(group) if decoder else group)
            else:
                for i in range(0, len(tokens), group_size):
                    group = tokens[i:i + group_size]
                    if group:
                        result.append(decoder(group) if decoder else group)
        else:
            if decoder:
                result.extend(decoder(token) for token in tokens)
            else:
                result.extend(tokens)
                
        return result
    
    
    def to_string(
            self, 
            separator:str|None=None,
            keep_sep:bool|None=None,
            encoder:ArrayEncoder|None=None
            ) -> str:
        
        keep_sep = keep_sep or self.KEEP_SEP
        encoder = encoder or self.ENCODER or str
        separator = '' if keep_sep else separator if separator is not None else self.SEPARATOR or ''
        return separator.join(encoder(x) for x in self)


class TypedDictMixin:
    
    KEY_TYPES: dict[str, Any] | None = None
    
    def coerce(self, key, value):
        key_type = self.KEY_TYPES.get(key)
        
        if callable(key_type):
            value = key_type(value)
        
        self[key] = value



class DictDefaultMixin:
    
    KEY_DEFAULTS: dict[str, Any] | None = None
    
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
    
    START_DELIMITER: str | None = None
    END_DELIMITER: str | None = None
    
    @classmethod
    def from_string(
            cls,
            string:str,
            *args,
            start_delimiter:str|None=None,
            end_delimiter:str|None=None,
            **kwargs
            ) -> Self:
        
        start_delimiter = start_delimiter if start_delimiter is not None else cls.START_DELIMITER
        end_delimiter = end_delimiter if end_delimiter is not None else cls.END_DELIMITER
        
        if start_delimiter: string = string.lstrip(start_delimiter)
        if end_delimiter: string = string.rstrip(end_delimiter)
        
        return super().from_string(string, *args, **kwargs)
    
    
    def to_string(
            self,
            *args,
            start_delimiter:str|None=None,
            end_delimiter:str|None=None,
            **kwargs
            ) -> Self:
        
        start_delimiter = start_delimiter if start_delimiter is not None else self.START_DELIMITER
        end_delimiter = end_delimiter if end_delimiter is not None else self.END_DELIMITER
        
        string = super().to_string(*args, **kwargs)
        if string:
            if start_delimiter: string = start_delimiter + string
            if end_delimiter: string = string + end_delimiter
        
        return string


class LoadFileMixin:
    
    DEFAULT_PATH: str | PathLike | None = None
    COMPRESSION: Literal['zlib', 'gzip', 'deflate'] | None = None
    CYPHER: bytes | None = None
    
    @classmethod
    def from_file(
            cls, 
            path:str|PathLike|None=None, 
            encoded:bool=True, 
            compression:Literal['zlib', 'gzip', 'deflate']|None=None, 
            cypher:bytes|None=None,
            **kwargs: Any
            ) -> Self:
        
        path = path or cls.DEFAULT_PATH
        compression = compression or cls.COMPRESSION
        cypher = cypher or cls.CYPHER
        
        if path is None:
            raise ValueError("path must be provided")
        
        with open(path, "r", encoding="utf-8") as file:
            
            string = file.read()
            
            if encoded: string = decode_string(string, compression=compression, xor_key=cypher)
            
            return super().from_string(string, **kwargs)
        
    
    def to_file(
            self,
            path:str|PathLike|None=None,
            compression:Literal['zlib', 'gzip', 'deflate']|None=None, 
            cypher:bytes|None=None,
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
