# Imports
from dataclasses import fields
from typing import Callable, Any, Self, Literal, Optional, TYPE_CHECKING, Iterable

# Package Imports
from gmdkit.serialization import options
from gmdkit.serialization.type_cast import (
    serialize, dict_serializer
)
from gmdkit.utils.typing import (
    PathString,
    StringDecoder, StringEncoder,
    StringDictDecoder, StringDictEncoder,
    PlistWrapper, DictWrapper, ArrayWrapper,
    Caster, DictCaster
)
from gmdkit.serialization.functions import (
    decompress_string, compress_string,
    from_plist_file, to_plist_file, 
    from_plist_string, to_plist_string,
    dict_wrapper, array_wrapper
)


class PlistDecoderMixin:
    
    ENCODER: Optional[Caster] = None
    DECODER: Optional[Caster] = None
    PLIST_FORMAT: Optional[PlistWrapper] = None
    SELF_FORMAT: Optional[PlistWrapper] = None
    path: Optional[PathString]
    
    
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
    
    @classmethod
    def from_tokens(
            cls,
            tokens:Iterable[str],
            list_format:Optional[bool]=None, 
            decoder:Optional[StringDictDecoder]=None
            ) -> Self:
        
        list_format = list_format if list_format is not None else cls.LIST_FORMAT
        decoder = decoder or cls.DECODER
        
        class_args = {}
        
        if list_format:
            for field, token in zip(fields(cls), tokens):
                try:
                    key, value = decoder(field.name, token)
                except Exception as e:
                    raise ValueError(
                        f"{cls.__module__}.{cls.__qualname__} failed to decode field '{field.name}' from token {token!r}"
                        ) from e
                class_args[key] = value
        else:
            length = len(tokens)
            if length % 2 != 0:
                raise ValueError(
                    f"{cls.__module__}.{cls.__qualname__} odd number of tokens: {length}"
                    )
            
            for i in range(0, length, 2):
                raw_key, raw_value = tokens[i], tokens[i + 1]
                try:
                    key, value = decoder(raw_key, raw_value)
                except Exception as e:
                    raise ValueError(
                        f"{cls.__module__}.{cls.__qualname__} failed to decode key/value at index {i}"
                        ) from e
                    
                if hasattr(cls, key):
                    class_args[key] = value
                else:
                    raise ValueError(
                        f"{cls.__module__}.{cls.__qualname__} unknown field '{key}'"
                        )
        
        return cls(**class_args)
        
    
    def to_tokens(
            self,
            list_format:Optional[bool]=None, 
            encoder:Optional[StringDictEncoder]=None
            ) -> Iterable[str]:
        
        list_format = list_format or self.LIST_FORMAT
        encoder = encoder or self.ENCODER
        
        parts = []
        for field in fields(self):
            value = getattr(self, field.name)
            try:
                key, encoded_value = encoder(field.name, value)
            except Exception as e:
                raise ValueError(
                    f"[{type(self).__module__}.{type(self).__qualname__}]"
                    f" Failed to encode field '{field.name}': {e}"
                    ) from e
                
            if not list_format:
                parts.append(key)
                
            parts.append(encoded_value)
            
        return parts

    
    @classmethod
    def from_string(
            cls, 
            string:str, 
            separator:Optional[str]=None, 
            list_format:Optional[bool]=None, 
            decoder:Optional[StringDictDecoder]=None
            ) -> Self:
        
        separator = separator if separator is not None else cls.SEPARATOR
        
        if not string:
            return cls()
        
        tokens = string.split(separator)
        
        return cls.from_tokens(
            tokens=tokens,
            list_format=list_format,
            decoder=decoder
            )

    
    def to_string(
            self, 
            separator:Optional[str]=None, 
            list_format:Optional[bool]=None, 
            encoder:Optional[StringDictEncoder]=None
            ) -> str:
        
        separator = separator if separator is not None else self.SEPARATOR
        
        parts = self.to_tokens(list_format=list_format, encoder=encoder)
        
        return separator.join(parts)
       
    
class DictDecoderMixin:
    
    SEPARATOR: str = ','
    ENCODER: Optional[StringDictEncoder] = staticmethod(dict_serializer)
    DECODER: Optional[StringDictDecoder] = None
    
    @classmethod
    def from_tokens(
            cls, 
            tokens:Iterable[str],
            decoder:Optional[StringDictDecoder]=None,
            condition:Optional[Callable]=None
            ) -> Self:
        
        decoder = decoder or cls.DECODER
        
        if len(tokens) % 2 != 0:
            raise ValueError(
                f"{cls.__module__}.{cls.__qualname__} odd number of tokens: {len(tokens)}"
                )
        
        result = cls()
        try:
            pairs = (decoder(k, v) for k, v in zip(tokens[::2], tokens[1::2]))
            result.update((k, v) for k, v in pairs if condition is None or condition(k, v))
        except Exception as e:
            raise ValueError(
                f"{cls.__module__}.{cls.__qualname__} failed to decode"
                ) from e
        
        return result
    
    
    def to_tokens(
            self, 
            encoder:Optional[StringDictEncoder]=None,
            condition:Optional[Callable]=None
            ) -> Iterable[str]:
        encoder = encoder or self.ENCODER
        
        try:
            return [
                part
                for key, value in self.items()
                if condition is None or condition(key, value)
                for part in encoder(key, value)
            ]
        except Exception as e:
            raise ValueError(
                f"{type(self).__module__}.{type(self).__qualname__} failed to encode"
                ) from e
            
    
    @classmethod
    def from_string(
            cls, 
            string:str, 
            separator:Optional[str]=None, 
            decoder:Optional[StringDictDecoder]=None,
            condition:Optional[Callable]=None
            ) -> Self:
        
        separator = separator if separator is not None else cls.SEPARATOR
        
        if string == "":
            return cls()
        
        tokens = string.split(separator)
        
        return cls.from_tokens(tokens,decoder=decoder,condition=condition)
    
    
    def to_string(
            self, 
            separator:Optional[str]=None, 
            encoder:Optional[StringDictEncoder]=None,
            condition:Optional[Callable]=None
            ) -> str:
        separator = separator or self.SEPARATOR
        
        parts = self.to_tokens(encoder=encoder,condition=condition)
        return separator.join(parts)
    

class ArrayDecoderMixin:
    
    SEPARATOR: str = ','
    KEEP_SEPARATOR: bool = False
    GROUP_SIZE: int = 1
    ENCODER: Optional[StringEncoder] = staticmethod(serialize)
    DECODER: Optional[StringDecoder] = None
    
    @classmethod
    def from_tokens(
            cls, 
            tokens:Iterable[str],
            group_size:Optional[int]=None, 
            decoder:Optional[StringDecoder]=None
            ) -> Self:
        
        group_size = group_size or cls.GROUP_SIZE
        decoder = decoder or cls.DECODER

        result = cls()
        
        try:
            if group_size > 1:
                for i in range(0, len(tokens), group_size):
                    result.append(decoder(tokens[i:i + group_size]) if decoder else tokens[i:i + group_size])
            elif decoder:
                result.extend(decoder(token) for token in tokens)
            else:
                result.extend(tokens)
        except Exception as e:
            raise ValueError(f"{cls.__module__}.{cls.__qualname__} failed to decode") from e
                
        return result
    
    
    def to_tokens(
            self,
            encoder:Optional[StringEncoder]=None,
            group_size:Optional[int]=None,
            ) -> str:
        
        encoder = encoder or self.ENCODER
        group_size = group_size or self.GROUP_SIZE
        
        tokens = []
        try:
            for x in self:
                if group_size > 1:
                    group = encoder(x)
                    if len(group) != group_size:
                        raise ValueError(f"encoder returned {len(group)} tokens, expected {self.GROUP_SIZE}")
                    tokens.extend(group)
                else:
                    tokens.append(encoder(x))
        except Exception as e:
            raise ValueError(f"{type(self).__module__}.{type(self).__qualname__} failed to encode") from e
        
        return tokens
    
    
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
        keep_sep = keep_sep or cls.KEEP_SEPARATOR

        result = cls()

        string = string.removeprefix(separator).removesuffix(separator)
        
        if not string:
            return result

        tokens = string.split(separator)
        
        if keep_sep:
            tokens = [token + separator for token in tokens]
                        
        return cls.from_tokens(
            tokens,
            group_size=group_size,
            decoder=decoder
            )
    
    
    def to_string(
            self, 
            separator:Optional[str]=None,
            keep_sep:Optional[bool]=None,
            group_size:Optional[int]=None, 
            encoder:Optional[StringEncoder]=None
            ) -> str:
        
        keep_sep = keep_sep or self.KEEP_SEPARATOR
        separator = '' if keep_sep else separator if separator is not None else self.SEPARATOR or ''
        
        tokens = self.to_tokens(encoder=encoder,group_size=group_size)
        
        return separator.join(tokens)



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
            
            if encoded: string = decompress_string(string, compression=compression, xor_key=cypher)
            
            new = super().from_string(string, **kwargs)
        
        new.path = path # ensure 'None' is replaced w/ valid path
        return new
        
    
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
        
        if path is None:
            raise ValueError("path must be provided")
        
        with open(path, "w", encoding="utf-8") as file:
            
            string = super().to_string(**kwargs)
            
            if encoded: string = compress_string(string, compression=compression, xor_key=cypher)
            
            file.write(string)
