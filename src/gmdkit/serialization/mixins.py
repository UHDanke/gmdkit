# Imports
from dataclasses import fields
from typing import Callable, Any, Self, get_type_hints, Literal, Optional, TYPE_CHECKING

# Package Imports
from gmdkit.serialization import options
from gmdkit.serialization.type_cast import (
    serialize, dict_serializer,
    dict_cast, 
    decode_funcs
)
from gmdkit.serialization.typing import (
    PathString,
    StringDecoder, StringEncoder,
    StringDictDecoder, StringDictEncoder,
    PlistWrapper, DictWrapper, ArrayWrapper,
    Caster, DictCaster
)
from gmdkit.serialization.functions import (
    decode_string, encode_string, 
    from_plist_file, to_plist_file, 
    from_plist_string, to_plist_string,
    dict_wrapper, array_wrapper
)


class PlistDecoderMixin:
    
    ENCODER: Optional[Caster] = None
    DECODER: Optional[Caster] = None
    PLIST_FORMAT: Optional[PlistWrapper] = None
    SELF_FORMAT: Optional[PlistWrapper] = None
    path: Optional[PathString] = None
    
    
    @classmethod
    def from_plist(
            cls, 
            data:Any, 
            decoder:Optional[Caster]=None,
            self_format:Optional[PlistWrapper]=None,
            **kwargs: Any
            ) -> Self:
        
        decoder = decoder or cls.DECODER
        self_format = self_format or cls.SELF_FORMAT
        
        if decoder is None or not callable(decoder) or self_format is None or not callable(self_format):
            return cls(data)
        
        new = self_format(data, decoder, **kwargs)
        
        return cls(new)
    
        
    def to_plist(
            self, 
            encoder:Optional[Caster]=None, 
            plist_format:Optional[PlistWrapper]=None,
            **kwargs
            ) -> Any:
        
        encoder = encoder or self.ENCODER
        plist_format = plist_format or self.PLIST_FORMAT
        
        if encoder is None or not callable(encoder) or plist_format is None or not callable(plist_format):
            return self

        new = plist_format(self, encoder, **kwargs)
        
        return new
    
    
    @classmethod
    def from_file(cls, path:PathString, **kwargs) -> Self:
        
        parsed = from_plist_file(path)
        
        new = cls.from_plist(parsed,**kwargs)
        new.path = path
                        
        return new
    
    
    def to_file(self, path:PathString, **kwargs):
            
        data = self.to_plist(**kwargs)
        
        to_plist_file(data, path)
    
    
    def update_file(self, **kwargs):
        self.to_file(path=self.path, **kwargs)
        
    
    @classmethod
    def from_string(cls, string:str, **kwargs) -> Self:
        
        parsed = from_plist_string(string)
        
        return cls.from_plist(parsed, **kwargs)
    
    
    def to_string(self, **kwargs) -> str:
        
        data = self.to_plist(**kwargs)
        
        return to_plist_string(data)


class PlistDictDecoderMixin(PlistDecoderMixin):
    
    ENCODER: Optional[DictCaster]
    DECODER: Optional[DictCaster] 
    PLIST_FORMAT: DictWrapper = staticmethod(dict_wrapper)
    SELF_FORMAT: DictWrapper = staticmethod(dict_wrapper)
    
    def reload_file(self, **kwargs) -> Self:
        new = type(self).from_file(path=self.path, **kwargs)
        self.clear()
        self.update(new)
        return self

    if TYPE_CHECKING:
        @classmethod
        def from_plist(
            cls, 
            data: dict, 
            decoder: Optional[DictCaster] = None, 
            self_format: Optional[DictWrapper] = None, 
            **kwargs: Any
        ) -> Self: ...
        
        def to_plist(
            self, 
            encoder: Optional[DictCaster] = None, 
            plist_format: Optional[DictWrapper] = None, 
            **kwargs
        ) -> dict: ...
        

class PlistArrayDecoderMixin(PlistDecoderMixin):
    
    ENCODER: Optional[Caster]
    DECODER: Optional[Caster] 
    PLIST_FORMAT: ArrayWrapper = staticmethod(array_wrapper)
    SELF_FORMAT: ArrayWrapper = staticmethod(array_wrapper)

    def reload_file(self, **kwargs) -> Self:
        new = type(self).from_file(path=self.path, **kwargs)
        self[:] = new
        return self

    if TYPE_CHECKING:
        @classmethod
        def from_plist(
            cls, 
            data: list, 
            decoder: Optional[Caster] = None, 
            self_format: Optional[ArrayWrapper] = None, 
            **kwargs: Any
        ) -> Self: ...
        
        def to_plist(
            self, 
            encoder: Optional[Caster] = None, 
            plist_format: Optional[ArrayWrapper] = None, 
            **kwargs
        ) -> list: ...


class DataclassDecoderMixin:
    
    SEPARATOR: str = ','
    LIST_FORMAT: bool = True
    ENCODER: Optional[StringDictEncoder] = staticmethod(dict_serializer)
    DECODER: Optional[StringDictDecoder] = None
    
    
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
            separator:Optional[str]=None, 
            list_format:Optional[bool]=None, 
            decoder:Optional[StringDictDecoder]=None
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
            separator:Optional[str]=None, 
            list_format:Optional[bool]=None, 
            encoder:Optional[StringDictEncoder]=None
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
    
    SEPARATOR: str = ','
    ENCODER: Optional[StringDictEncoder] = staticmethod(dict_serializer)
    DECODER: Optional[StringDictDecoder] = None
    
    @classmethod
    def from_string(
            cls, 
            string:str, 
            separator:Optional[str]=None, 
            decoder:Optional[StringDictDecoder]=None,
            condition:Optional[Callable]=None
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
            separator:Optional[str]=None, 
            encoder:Optional[StringDictEncoder]=None,
            condition:Optional[Callable]=None
            ) -> str:
        separator = separator or self.SEPARATOR
        encoder = encoder or self.ENCODER
        
        parts = []
        for key, value in self.items():
            if condition is None or condition(key, value):
                parts.extend(encoder(key, value))
        
        return separator.join(parts)
    

class ArrayDecoderMixin:
    
    SEPARATOR: str = ','
    KEEP_SEP: bool = False
    GROUP_SIZE: int = 1
    ENCODER: Optional[StringEncoder] = staticmethod(serialize)
    DECODER: Optional[StringDecoder] = None
    
    @classmethod
    def from_string(
            cls, 
            string:str, 
            separator:Optional[str]=None,
            keep_sep:Optional[bool]=None,
            group_size:Optional[int]=None, 
            decoder:Optional[StringDecoder]=None
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
            separator:Optional[str]=None,
            keep_sep:Optional[bool]=None,
            encoder:Optional[StringEncoder]=None
            ) -> str:
        
        keep_sep = keep_sep or self.KEEP_SEP
        encoder = encoder or self.ENCODER or str
        separator = '' if keep_sep else separator if separator is not None else self.SEPARATOR or ''
        return separator.join(encoder(x) for x in self)


class TypeDictMixin:
    
    KEY_TYPES: dict[Any, Callable] | None = None
    TYPE_DEFAULT: Callable = str
    
    def key_type(self, key:Any):
        kt = self.KEY_TYPES.get(key)
        
        if kt is not None:
            return kt
        else:
            return self.TYPE_DEFAULT
        
    def coerce(self, key, value):
        kt = self.key_type(key)
        self[key] = kt(value)
        
    def coerce_dict(self, dictionary:dict):
        for k, v in dictionary.items():
            self.coerce(k,v)


class DictDefaultMixin(TypeDictMixin):
    
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
    
    START_DELIMITER: Optional[str] = None
    END_DELIMITER: Optional[str] = None
    
    @classmethod
    def from_string(
            cls,
            string:str,
            *args,
            start_delimiter:Optional[str]=None,
            end_delimiter:Optional[str]=None,
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
            start_delimiter:Optional[str]=None,
            end_delimiter:Optional[str]=None,
            **kwargs
            ) -> str:
        
        start_delimiter = start_delimiter if start_delimiter is not None else self.START_DELIMITER
        end_delimiter = end_delimiter if end_delimiter is not None else self.END_DELIMITER
        
        string = super().to_string(*args, **kwargs)
        if string:
            if start_delimiter: string = start_delimiter + string
            if end_delimiter: string = string + end_delimiter
        
        return string


class CompressFileMixin:
    
    DEFAULT_PATH: Optional[PathString] = None
    COMPRESSION: Optional[Literal['zlib', 'gzip', 'deflate']] = None
    CYPHER: Optional[bytes] = None
    
    @classmethod
    def from_file(
            cls, 
            path:Optional[PathString]=None, 
            encoded:bool=True, 
            compression:Optional[Literal['zlib', 'gzip', 'deflate']]=None, 
            cypher:Optional[bytes]=None,
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
            path:Optional[PathString]=None,
            compression:Optional[Literal['zlib', 'gzip', 'deflate']]=None, 
            cypher:Optional[bytes]=None,
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
