# Imports
from pathlib import Path
from dataclasses import fields
import xml.etree.ElementTree as ET
from typing import (
    Any, Self, Literal, 
    Optional, 
    Callable, Sequence,
    )

import glob

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
    PlistDecoder,PlistEncoder
)
from gmdkit.serialization.functions import (
    decompress_string, compress_string,
    read_plist, write_plist,
    validate_dict_node
)


class PlistDecoderMixin:
    
    ENCODER: Optional[PlistEncoder] = None
    DECODER: Optional[PlistDecoder] = None
    CONTAINER: Optional[str] = None
    ENCODER_KEY: Optional[int] = None
    IS_ARRAY: bool = False
    node: ET.Element
    path: PathString
    
    
    def load_data(
            self,
            node:Optional[ET.Element]=None, 
            is_array:Optional[bool]=None,
            encoder_key:Optional[int]=None,
            decoder:Optional[PlistEncoder]=None,
            container:Optional[int]=None,
            **kwargs
            ):
        
        node = self.node if node is None else node
        is_array = self.IS_ARRAY if is_array is None else is_array
        encoder_key = self.ENCODER_KEY if encoder_key is None else encoder_key
        decoder = self.DECODER if decoder is None else decoder
        container = self.CONTAINER if container is None else container
        data = self if container is None else getattr(self, container)
        
        try:
            validate_dict_node(node, is_array=is_array, encoder_key=encoder_key)
        except Exception as e:
            raise RuntimeError(f"{type(self).__module__}.{type(self).__qualname__} failed to validate node") from e
        
        data.clear()
        
        start = 2 if is_array or encoder_key is not None else 0
        index_range = range(start, len(node), 2)
        
        if decoder:
            if is_array:
                data.extend(decoder(node[i+1],**kwargs) for i in index_range)
            else:
                data.update(decoder(node[i].text,node[i+1],**kwargs) for i in index_range)
        else:
            if is_array:
                data.extend(read_plist(node[i+1]) for i in index_range)
            else:
                data.update((node[i].text, read_plist(node[i+1])) for i in index_range)

    
    def save_data(
            self,
            node:Optional[ET.Element]=None,
            is_array:Optional[bool]=None,
            encoder_key:Optional[int]=None,
            encoder:Optional=None,
            container:Optional[int]=None,
            **kwargs):
        
        node = self.node if node is None else node
        is_array = self.IS_ARRAY if is_array is None else is_array
        encoder_key = self.ENCODER_KEY if encoder_key is None else encoder_key
        encoder = self.ENCODER if encoder is None else encoder
        container = self.CONTAINER if container is None else container
        data = self if container is None else getattr(self, container)
        
        node[:] = []
        
        if is_array:
            ET.SubElement(node, 'k').text = '_isArr'
            ET.SubElement(node, 't')
            items = enumerate(data, start=1)
            if encoder:
                def write(k, v): return f'k_{k}', encoder(v, **kwargs)
            else:
                def write(k, v): return f'k_{k}', write_plist(v)
        else:
            if encoder_key is not None:
                ET.SubElement(node, 'k').text = 'kCEK'
                ET.SubElement(node, 'i').text = str(encoder_key)
            items = data.items()
            if encoder:
                def write(k, v): return encoder(k, v, **kwargs)
            else:
                def write(k, v): return k, write_plist(v)
    
        sub = ET.SubElement
        append = node.append
    
        for k, v in items:
            k, v = write(k, v)
            if v is None:
                continue
            sub(node, 'k').text = k
            append(v)
    
        return node
    
    
    @classmethod
    def from_node(cls, node:ET.Element, load_data:bool=True, **kwargs):
        
        new = cls()
        new.node = node
        try:
            if node.tag == "dict":
                node.tag = "d"
            if load_data:
                new.load_data(**kwargs)
        except:
            print(node)
            raise RuntimeError(f"{cls.__module__}.{cls.__qualname__}")
        return new
    
    def to_node(self, save_data:bool=True, **kwargs):
        
        if save_data:
            self.save_data(**kwargs)
        
        return self.node

    @classmethod
    def from_string(cls, string:str, **kwargs):
        
        node = ET.fromstring(string)
        
        if node.tag != "plist":
            raise ValueError(f"Expected root node to be plist, got '{node.tag}'")
        
        root = node.find("dict")
        
        if root is None:
            raise ValueError("plist does not contain a <dict> root element")
        
        return cls.from_node(root,**kwargs)
    
    
    def to_string(self, xml_declaration:bool=True, **kwargs):
        node = self.to_node(**kwargs)

        tag = node.tag
        node.tag = "dict"
        
        root = ET.Element("plist", version="1.0", gjver="2.0")
        root.append(node)
        
        string = ET.tostring(
            root,
            encoding="unicode",
            xml_declaration=xml_declaration
        )
        
        node.tag = tag
        
        return string
    
    
    @classmethod
    def from_file(cls, path:PathString, **kwargs) -> Self:
        
        with open(path, "r") as file:
            string = file.read()
            
        new = cls.from_string(string, **kwargs)
        new.path = path
        return new
    
    
    def to_file(self, 
            path:Optional[PathString]=None, 
            **kwargs):
        
        path = path or getattr(self, "path", None)
        
        string = self.to_string(**kwargs)
        
        with open(path,"w") as file:
            file.write(string)
    
    
    def update_file(self, **kwargs):
        self.to_file(path=self.path, **kwargs)
        
        
    def reload_file(self, load_data:bool=True, **kwargs):
        new = self.from_file(path=self.path, load_data=False)
        
        self.node = new.node
        
        if load_data:
            self.load_data(**kwargs)
        

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
            decoder:Optional[StringDictDecoder]=None,
            decoder_kwargs:bool=False,
            **kwargs
            ) -> Self:
        
        from_array = cls.FROM_ARRAY if from_array is None else from_array
        decoder = cls.DECODER if decoder is None else decoder
        
        class_args = {}
        f = fields(cls)
        f_len = len(f) * (1 if from_array else 2)
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
                        if decoder_kwargs:
                            key, value = decoder(encoded_key, encoded_value, **kwargs)
                        else:
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
        
        from_array = self.FROM_ARRAY if from_array is None else from_array
        condition = self.CONDITION if condition is None else condition
        encoder = self.ENCODER if encoder is None else encoder
        
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
        
        separator = cls.SEPARATOR if separator is None else separator
        max_split = cls.MAX_SPLIT if max_split is None else max_split
        
        if not string:
            return cls()
        
        if not separator:
            tokens = [*string[:max_split], string[max_split:]] if max_split is not None else list(string)
        else:
            tokens = string.split(separator, -1 if max_split is None else max_split)
        
        return cls.from_tokens(tokens,**kwargs)
            
        
    def to_string(
            self, 
            separator:Optional[str]=None, 
            **kwargs
            ) -> str:
        
        separator = self.SEPARATOR if separator is None else separator
        
        parts = self.to_tokens(**kwargs)
        
        return separator.join(parts)


class DictDecoderMixin:
    
    SEPARATOR: str = ','
    ENCODER: Optional[StringDictEncoder] = staticmethod(dict_serializer)
    DECODER: Optional[StringDictDecoder] = None
    CONTAINER: Optional[str] = None
    CONDITION: Optional[KeyValueCondition] = None
    
    @classmethod
    def from_tokens(
            cls, 
            tokens:Sequence[str],
            decoder:Optional[StringDictDecoder]=None,
            container:Optional[str]=None
            ) -> Self:
        
        decoder = cls.DECODER if decoder is None else decoder
        container = cls.CONTAINER if container is None else container
        
        if len(tokens) % 2 != 0:
            raise ValueError(
                f"{cls.__module__}.{cls.__qualname__} odd number of tokens: {len(tokens)}"
                )
            
        result = cls()
        
        if container is None:
            data = result
        else:
            data = getattr(result, container)
            
        if decoder is None:
            data.update(zip(tokens[::2], tokens[1::2]))
        else:
            try:
                data.update(decoder(k, v) for k, v in zip(tokens[::2], tokens[1::2]))
            except Exception as e:
                raise ValueError(
                    f"{cls.__module__}.{cls.__qualname__} failed to decode"
                    ) from e
        
        return result
    
    
    def to_tokens(
            self, 
            encoder:Optional[StringDictEncoder]=None,
            condition:Optional[KeyValueCondition]=None,
            container:Optional[str]=None
            ) -> Sequence[str]:
        
        encoder = self.ENCODER if encoder is None else encoder
        condition = self.CONDITION if condition is None else condition
        container = self.CONTAINER if container is None else container
        
        if container is None:
            data = self
        else:
            data = getattr(self, container)
            
        try:
            return [
                part
                for key, value in data.items()
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
        
        separator = cls.SEPARATOR if separator is None else separator
        
        if string == "":
            return cls()
        
        tokens = list(string) if not separator else string.split(separator)
        
        return cls.from_tokens(tokens,**kwargs)
    
    
    def to_string(
            self, 
            separator:Optional[str]=None, 
            **kwargs
            ) -> str:
        separator = self.SEPARATOR if separator is None else separator
        
        parts = self.to_tokens(**kwargs)
        return separator.join(parts)


class ArrayDecoderMixin:
    
    SEPARATOR: str = ','
    KEEP_SEPARATOR: bool = False
    GROUP_SIZE: int = 1
    ENCODER: Optional[StringEncoder] = staticmethod(serialize)
    DECODER: Optional[StringDecoder] = None
    CONTAINER: Optional[str] = None
    
    @classmethod
    def from_tokens(
            cls, 
            tokens:Sequence[str],
            decoder:Optional[StringDecoder]=None,
            group_size:Optional[int]=None,
            container:Optional[str]=None
            ) -> Self:
        
        decoder = cls.DECODER if decoder is None else decoder
        group_size = cls.GROUP_SIZE if group_size is None else group_size
        container = cls.CONTAINER if container is None else container
        
        result = cls()
        
        if container is None:
            data = result
        else:
            data = getattr(result, container)
        
        try:
            if group_size > 1:
                for i in range(0, len(tokens), group_size):
                    data.append(decoder(tokens[i:i + group_size]) if decoder else tokens[i:i + group_size])
            elif decoder:
                data.extend(decoder(token) for token in tokens)
            else:
                data.extend(tokens)
        except Exception as e:
            raise ValueError(f"{cls.__module__}.{cls.__qualname__} failed to decode") from e
                
        return result
    
    
    def to_tokens(
            self,
            encoder:Optional[StringEncoder]=None,
            group_size:Optional[int]=None,
            container:Optional[str]=None
            ) -> Sequence[str]:
        
        encoder = self.ENCODER if encoder is None else encoder
        group_size = self.GROUP_SIZE if group_size is None else group_size
        container = self.CONTAINER if container is None else container
        
        if container is None:
            data = self
        else:
            data = getattr(self, container)
        
        tokens = []
        try:
            if group_size > 1:
                for x in data:
                    group = encoder(x) if encoder else x
                    if len(group) != group_size:
                        raise ValueError(f"encoder returned {len(group)} tokens, expected {group_size}")
                    tokens.extend(group)
            elif encoder:
                tokens.extend(encoder(x) for x in data)
            else:
                tokens.extend(data)
                
        except Exception as e:
            raise ValueError(f"{type(self).__module__}.{type(self).__qualname__} failed to encode") from e
        
        return tokens
    
    
    @classmethod
    def from_string(
            cls, 
            string:str, 
            separator:Optional[str]=None,
            keep_separator:Optional[bool]=None,
            **kwargs
            ) -> Self:
        
        separator = cls.SEPARATOR if separator is None else separator
        keep_separator = cls.KEEP_SEPARATOR if keep_separator is None else keep_separator
        
        result = cls()
        
        if not string:
            return result
        
        if keep_separator:
            string = string.removesuffix(separator)
        
        tokens = list(string) if not separator else string.split(separator)
           
        if keep_separator and separator:
            tokens = [token + separator for token in tokens]
                        
        return cls.from_tokens(tokens,**kwargs)
    
    
    def to_string(
            self, 
            separator:Optional[str]=None,
            keep_separator:Optional[bool]=None,
            **kwargs
            ) -> str:
        separator = self.SEPARATOR if separator is None else separator        
        keep_separator = self.KEEP_SEPARATOR if keep_separator is None else keep_separator
        separator = '' if keep_separator else separator
        
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
        
        start_delimiter = cls.START_DELIMITER if start_delimiter is None else start_delimiter
        end_delimiter = cls.END_DELIMITER if end_delimiter is None else end_delimiter
        
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
        
        start_delimiter = self.START_DELIMITER if start_delimiter is None else start_delimiter
        end_delimiter = self.END_DELIMITER if end_delimiter is None else end_delimiter
        
        string = super().to_string(*args, **kwargs)
        if string:
            if start_delimiter: string = start_delimiter + string
            if end_delimiter: string = string + end_delimiter
        
        return string


class CompressFileMixin:
    
    COMPRESSED: bool = False
    COMPRESSION: Optional[Literal['zlib', 'gzip', 'deflate']] = None
    CYPHER: Optional[bytes] = None
    
    @classmethod
    def from_string(
            cls,
            string:str,
            compressed:Optional[bool]=None,
            compression:Optional[Literal['zlib', 'gzip', 'deflate']]=None,
            cypher:Optional[bytes]=None,
            **kwargs
            ) -> Self:
        
        compressed = cls.COMPRESSED if compressed is None else compressed
        compression = cls.COMPRESSION if compression is None else compression
        cypher = cls.CYPHER if cypher is None else cypher
        
        if compressed:
            string = decompress_string(string, compression=compression, xor_key=cypher)
            
        return super().from_string(string, **kwargs)
    
    
    def to_string(
            self,
            compressed:Optional[bool]=None,
            compression:Optional[Literal['zlib', 'gzip', 'deflate']]=None,
            cypher:Optional[bytes]=None,
            **kwargs
            ) -> str:
        
        compressed = self.COMPRESSED if compressed is None else compressed
        compression = self.COMPRESSION if compression is None else compression
        cypher = self.CYPHER if cypher is None else cypher
        
        string = super().to_string(**kwargs)
    
        if compressed:
            string = compress_string(string, compression=compression, xor_key=cypher)
        
        return string
        

class FilePathMixin:
    
    EXTENSION: Optional[str] = None
    DEFAULT_PATH: Optional[PathString] = None
    
    def _name_fallback_(self):
        raise ValueError("No name fallback provided")
    
    @classmethod
    def from_file(
            cls, 
            path:Optional[PathString]=None,
            extension:Optional[str]=None,
            **kwargs: Any
            ) -> Self:
        
        path = cls.DEFAULT_PATH if path is None else path
        extension = cls.EXTENSION if extension is None else extension
        
        if path is None:
            path = Path()
        else:
            path = Path(path)
        
        path_ext = (path.suffix or "").removeprefix(".")
        
        if extension is not None and path_ext != extension:
            raise ValueError(f"Wrong extension, expected '{extension}', got '{path_ext}'")
            
        return super().from_file(path=path,**kwargs)
      
    
    def to_file(self, 
            path:Optional[PathString]=None, 
            extension:Optional[str]=None,
            **kwargs):
        
        path = self.DEFAULT_PATH if path is None else path
        extension = self.EXTENSION if extension is None else extension
        
        if path is None: 
            path = Path()
        else:
            path = Path(path)
            
        path_ext = (path.suffix or "").removeprefix(".")
        
        if extension is not None and path_ext != extension:
            raise ValueError(f"Wrong extension, expected '{extension}', got '{path_ext}'")
            
        if not path.suffix:
            name = self._name_fallback_()
            if name is None:
                raise ValueError("Cannot resolve default filename as fallback returned None")
                
            path = (path / name).with_suffix('.' + extension)
        
        super().to_file(path=path)
        

class LoadContentMixin:
    
    CONTENT_KEYS: Optional[set] = None
    
    @classmethod
    def from_node(cls, node:ET.Element, load_content:bool=True, content_keys:Optional[set]=None, **kwargs):
        
        new = super().from_node(node, **kwargs)
        
        if load_content: 
            new.load_content(content_keys=content_keys)
            
        return new
    
    
    def to_node(self, save_content:bool=True, content_keys:Optional[set]=None, **kwargs):
        
        if save_content:
            self.save_content(content_keys=content_keys)
        
        return super().to_node(**kwargs)

        
    def load_content(self, content_keys:Optional[set]=None):
        
        target = content_keys if content_keys is not None else getattr(self, "CONTENT_KEYS", None)
    
        available = self.keys()
        if target is not None:
            key_set = available & target
        else:
            key_set = available
        
        for key in key_set:
            value = self.get(key)
            load = getattr(value, "load", None)
    
            if load is not None and callable(load):
                load()
        
            
    def save_content(self, content_keys:Optional[set]=None):
        
        target = content_keys if content_keys is not None else getattr(self, "CONTENT_KEYS", None)
    
        available = self.keys()
        if target is not None:
            key_set = available & target
        else:
            key_set = available
            
        for key in key_set:
            value = self.get(key)
            save = getattr(value, "save", None)
    
            if save is not None and callable(save):
                save()


class FolderLoaderMixin:
    
    FOLDER_DECODER: Optional[Callable] = None
    FOLDER_ENCODER: Optional[Callable] = None
    FOLDER_EXTENSION: Optional[str] = None
    CONTAINER: Optional[str] = None
    
    @classmethod
    def from_folder(
            cls, 
            path:PathString, 
            extension:Optional[str]=None,
            decoder:Optional[Callable]=None,
            container:Optional[str]=None,
            **kwargs
            ):
        
        extension = cls.FOLDER_EXTENSION if extension is None else extension
        decoder = cls.FOLDER_DECODER if decoder is None else decoder
        container = cls.CONTAINER if container is None else container
        
        new = cls()
        
        if container is None:
            data = new
        else:
            data = getattr(new, container)
        
        folder_path = str(Path(path) / ('*.' + extension))
        
        for file_path in glob.glob(folder_path):
            item = decoder(file_path, **kwargs)
            data.append(item)
        
        return new
    
    
    def to_folder(
            self, 
            path:PathString,
            encoder:Optional[Callable]=None,
            container:Optional[str]=None,
            ):
        
        encoder = self.FOLDER_ENCODER if encoder is None else encoder
        container = self.CONTAINER if container is None else container
        
        if container is None:
            data = self
        else:
            data = getattr(self, container)
            
        folder_path = Path(path)
        
        if not folder_path.is_dir():
            raise ValueError("Given path is not a directory.")
        
        for item in data:
            encoder(item, folder_path)
            