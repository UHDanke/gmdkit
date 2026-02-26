# Imports
from dataclasses import fields
import xml.etree.ElementTree as ET
from typing import (
    Any, Self, Literal, 
    Optional, 
    Callable, Sequence,
    TYPE_CHECKING,
    )

# Package Imports
from gmdkit.serialization import options
from gmdkit.serialization.type_cast import (
    serialize, dict_serializer
)
from gmdkit.utils.typing import (
    PathString,
    StringDecoder, StringEncoder,
    StringDictDecoder, StringDictEncoder,
    KeyValueCondition,
    PlistWrapper, DictWrapper, ArrayWrapper,
    Caster, DictCaster
)
from gmdkit.serialization.functions import (
    decompress_string, compress_string,
    from_plist_file, to_plist_file, 
    from_plist_string, to_plist_string,
    read_plist, write_plist,
    dict_wrapper, array_wrapper,
    validate_dict_node
)


class PlistMixin:
    
    ENCODER: Optional[DictCaster]
    DECODER: Optional[DictCaster]
    ENCODER_KEY: Optional[int] = None
    IS_ARRAY: bool = False
    node: Optional[ET.Element]
    path: Optional[PathString]
    
    
    def __init_subclass__(cls, **kwargs):
       super().__init_subclass__(**kwargs)
       
       if cls.IS_ARRAY and cls.ENCODER_KEY is not None:
           raise TypeError(f"{cls.__module__}.{cls.__qualname__}: IS_ARRAY and ENCODER_KEY are mutually exclusive")    
    
    
    def load_plist(
            self,
            node:Optional[ET.Element]=None, 
            is_array:Optional[bool]=None,
            encoder_key:Optional[int]=None,
            decoder:Optional=None,            
            **kwargs
            ):
        
        node = node if node is not None else self.node
        is_array = self.IS_ARRAY
        encoder_key = self.ENCODER_KEY
        decoder = self.DECODER
        
        try:
            validate_dict_node(node, is_array, encoder_key)
        except Exception as e:
            raise RuntimeError(f"{type(self).__module__}.{type(self).__qualname__} failed to validate node") from e
        
        self.clear()
        
        start = 2 if is_array or encoder_key is not None else 0
        index_range = range(start, len(node), 2)
        
        if decoder:
            if is_array:
                self.extend(decoder(node[i+1].text,**kwargs) for i in index_range)
            else:
                self.update(decoder(node[i].text,node[i+1].text,**kwargs) for i in index_range)
        else:
            if is_array:
                self.extend(read_plist(node[i+1]) for i in index_range)
            else:
                self.update((node[i].text, read_plist(node[i+1])) for i in index_range)

    
    def save_plist(
            self,
            node:Optional[ET.Element]=None,
            is_array:Optional[bool]=None,
            encoder_key:Optional[int]=None,
            encoder:Optional=None,
            **kwargs):
        
        node = node if node is not None else self.node
        is_array = self.IS_ARRAY
        encoder_key = self.ENCODER_KEY
        encoder = self.ENCODER
        
        node[:] = []
        
        # headers
        if is_array:
            ET.SubElement(node, 'k').text = '_isArr'
            ET.SubElement(node, 't')
        elif encoder_key is not None:
            ET.SubElement(node, 'k').text = 'kCEK'
            ET.SubElement(node, 'i').text = str(encoder_key)
        
        if is_array:
            for k, v in enumerate(self, start=1):
                if encoder is not None:
                    v = encoder(v, **kwargs)
                ET.SubElement(node, 'k').text = f'k_{k}'
                write_plist(node,v)
        else:
            for k, v in self.items():
                if encoder is not None:
                    k, v = encoder(k, v, **kwargs)
                
                ET.SubElement(node, 'k').text = k
                write_plist(node, v)

        return node


    @classmethod
    def from_string(cls, string:str, **kwargs):
        
        node = ET.fromstring(string)
        
        if node.tag != "plist":
            raise ValueError("Expected root node to be plist, got '{node.tag}'")
        
        root = node.find("dict")
        
        new = cls()
        new.node = root
        new.load_plist()
        
        return new
    
    
    def to_string(self, **kwargs):
        
        root = ET.Element("plist", version="1.0", gjver="2.0")
        
        pass
    
    
    @classmethod
    def from_file(cls, path:PathString, **kwargs) -> Self:
        
        with open(path) as file:
            string = file.read()
            
        new = cls.from_string(string, **kwargs)
        new.path = path
                        
        return new
    
    
    def to_file(self, path:PathString, **kwargs):
            
        data = self.to_plist(**kwargs)
        
        to_plist_file(data, path)
    
    
    def update_file(self, **kwargs):
        self.to_file(path=self.path, **kwargs)
        
    

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
        
        if encoder is None or not callable(encoder) or plist_format is None:
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
    MAX_SPLIT: Optional[int] = None
    FROM_ARRAY: bool = True
    ENCODER: Optional[StringDictEncoder] = staticmethod(dict_serializer)
    DECODER: Optional[StringDictDecoder] = None
    CONDITION: Optional[KeyValueCondition] = None
    
    @classmethod
    def from_tokens(
            cls,
            tokens:Sequence[str],
            from_array:Optional[bool]=None, 
            decoder:Optional[StringDictDecoder]=None
            ) -> Self:
        
        from_array = from_array if from_array is not None else cls.FROM_ARRAY
        decoder = decoder or cls.DECODER
        
        class_args = {}
        f = fields(cls)
        f_len = len(f) * 1 if from_array else 2
        length = len(tokens)
        
        if length > f_len:
            raise ValueError(
                f"{cls.__module__}.{cls.__qualname__} too many tokens: {length}, expected at most {f_len}"
                )
        
        if from_array:            
            for field, token in zip(f, tokens):
                try:
                    key, value = decoder(field.name, token)
                except Exception as e:
                    raise ValueError(
                        f"{cls.__module__}.{cls.__qualname__} failed to decode field '{field.name}'"
                        ) from e
                class_args[key] = value
        else:
            if length % 2 != 0:
                raise ValueError(
                    f"{cls.__module__}.{cls.__qualname__} odd number of tokens: {length}"
                    )            
                
            for i in range(0, length, 2):
                encoded_key, encoded_value = tokens[i], tokens[i + 1]
                
                if decoder is None:
                    key = encoded_key
                    value = encoded_value
                else:
                    try:
                        key, value = decoder(encoded_key, encoded_value)
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
            from_array:Optional[bool]=None,
            condition:Optional[Callable]=None,
            encoder:Optional[StringDictEncoder]=None
            ) -> Sequence[str]:
        
        from_array = from_array if from_array is not None else self.FROM_ARRAY
        condition = condition or self.CONDITION
        encoder = encoder or self.ENCODER
        
        parts = []
        
        field_data = tuple(
            (field.name, getattr(self, field.name))
            for field in fields(self)
        )
        
        skip_fields = set()
        if condition is not None:
            for key, value in reversed(field_data):
                if condition(key, value):
                    skip_fields.add(key)
                elif from_array:
                    break
                    
        for key, value in field_data:
            
            if skip_fields and key in skip_fields:
                continue
            
            if encoder is None:
                encoded_key = key
                encoded_value = value
            else:
                try:
                    encoded_key, encoded_value = encoder(key, value)
                except Exception as e:
                    raise ValueError(
                        f"[{type(self).__module__}.{type(self).__qualname__}]"
                        f" Failed to encode field '{key}': {e}"
                        ) from e
                    
            if not from_array:
                parts.append(encoded_key)
                
            parts.append(encoded_value)
            
        return parts
    
        
    @classmethod
    def from_string(
            cls, 
            string:str, 
            separator:Optional[str]=None,
            max_split:Optional[int]=None,
            **kwargs
            ) -> Self:
        
        separator = separator if separator is not None else cls.SEPARATOR
        max_split = max_split if max_split is not None else cls.MAX_SPLIT
        
        if not string:
            return cls()
        
        tokens = string.split(separator, max_split)
        
        return cls.from_tokens(tokens,**kwargs)
            
        
    def to_string(
            self, 
            separator:Optional[str]=None, 
            **kwargs
            ) -> str:
        
        separator = separator if separator is not None else self.SEPARATOR
        
        parts = self.to_tokens(**kwargs)
        
        return separator.join(parts)


class DictDecoderMixin:
    
    SEPARATOR: str = ','
    ENCODER: Optional[StringDictEncoder] = staticmethod(dict_serializer)
    DECODER: Optional[StringDictDecoder] = None
    CONDITION: Optional[KeyValueCondition] = None
    
    @classmethod
    def from_tokens(
            cls, 
            tokens:Sequence[str],
            decoder:Optional[StringDictDecoder]=None,
            ) -> Self:
        
        decoder = decoder or cls.DECODER
        
        if len(tokens) % 2 != 0:
            raise ValueError(
                f"{cls.__module__}.{cls.__qualname__} odd number of tokens: {len(tokens)}"
                )
        
        result = cls()
        if decoder is None:
            result.update(zip(tokens[::2], tokens[1::2]))
        else:
            try:
                result.update(decoder(k, v) for k, v in zip(tokens[::2], tokens[1::2]))
            except Exception as e:
                raise ValueError(
                    f"{cls.__module__}.{cls.__qualname__} failed to decode"
                    ) from e
        
        return result
    
    
    def to_tokens(
            self, 
            encoder:Optional[StringDictEncoder]=None,
            condition:Optional[KeyValueCondition]=None
            ) -> Sequence[str]:
        encoder = encoder or self.ENCODER
        condition = condition or self.CONDITION
        
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
            **kwargs,
            ) -> Self:
        
        separator = separator if separator is not None else cls.SEPARATOR
        
        if string == "":
            return cls()
        
        tokens = string.split(separator)
        
        return cls.from_tokens(tokens,**kwargs)
    
    
    def to_string(
            self, 
            separator:Optional[str]=None, 
            **kwargs
            ) -> str:
        separator = separator or self.SEPARATOR
        
        parts = self.to_tokens(**kwargs)
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
            tokens:Sequence[str],
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
            ) -> Sequence[str]:
        
        encoder = encoder or self.ENCODER
        group_size = group_size or self.GROUP_SIZE
        
        tokens = []
        try:
            if group_size > 1:
                for x in self:
                    group = encoder(x) if encoder else x
                    if len(group) != group_size:
                        raise ValueError(f"encoder returned {len(group)} tokens, expected {group_size}")
                    tokens.extend(group)
            elif encoder:
                tokens.extend(encoder(token) for token in tokens)
            else:
                tokens.extend(tokens)
                
        except Exception as e:
            raise ValueError(f"{type(self).__module__}.{type(self).__qualname__} failed to encode") from e
        
        return tokens
    
    
    @classmethod
    def from_string(
            cls, 
            string:str, 
            separator:Optional[str]=None,
            keep_sep:Optional[bool]=None,
            **kwargs
            ) -> Self:
        
        separator = separator if separator is not None else cls.SEPARATOR
        keep_sep = keep_sep if keep_sep is not None else cls.KEEP_SEPARATOR
        
        result = cls()
        
        string = string.removeprefix(separator).removesuffix(separator)
        
        if not string:
            return result
        
        tokens = string.split(separator)
           
        if keep_sep:
            tokens = [token + separator for token in tokens]
                        
        return cls.from_tokens(tokens,**kwargs)
    
    
    def to_string(
            self, 
            separator:Optional[str]=None,
            keep_sep:Optional[bool]=None,
            **kwargs
            ) -> str:
        
        keep_sep = keep_sep if keep_sep is not None else self.KEEP_SEPARATOR
        separator = '' if keep_sep else separator if separator is not None else self.SEPARATOR or ''
        
        tokens = self.to_tokens(**kwargs)
        
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
        
        if start_delimiter: string = string.removeprefix(start_delimiter)
        if end_delimiter: string = string.removesuffix(end_delimiter)
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


class PlistOutputMixin:

    EXTENSION: str="plist"
    FALLBACK_NAME: Callable = lambda self: self[lvl_prop.NAME]
    
    def to_file(self, 
            path:Optional[PathString]=None, 
            extension:Optional[str]=None,
            fallback_name:Optional[Callable]=None,
            **kwargs):
        
        fallback_name = fallback_name is not None or self.FALLBACK_NAME
        
        if path is None: 
            path = Path()
        else:
            path = Path(path)
        
        if not path.suffix:
            name = fallback_name(self)
            path = (path / name).with_suffix('.' + extension.lstrip('.'))
            
        super().to_file(path=path, **kwargs)