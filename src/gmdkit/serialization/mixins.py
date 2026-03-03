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
    validate_dict_node, get_plist_root
)


class FileStringMixin:
    
    @classmethod
    def from_file(cls, path:PathString, encoding="utf-8", **kwargs) -> Self:
        
        with open(path, "r", encoding=encoding) as file:
            string = file.read()
            
        new = cls.from_string(string, **kwargs)
        new.path = path
        return new
    
    
    def to_file(self, path:PathString, encoding="utf-8", **kwargs):
        
        string = self.to_string(**kwargs)
        
        with open(path, "w", encoding=encoding) as file:
            file.write(string)


class DefaultPathMixin:
    
    DEFAULT_PATH: Optional[PathString] = None
    
    @classmethod
    def from_default_path(cls, **kwargs) -> Self:
        
        path = cls.DEFAULT_PATH
        
        if path is None:
            raise ValueError("[{cls.__name__}] default path does not exist")
        
        return cls.from_file(path,**kwargs)
    
    
    def to_default_path(self, **kwargs):
        
        path = type(self).DEFAULT_PATH
        
        if path is None:
            raise ValueError("[{type(self).__name__}]  default path does not exist")
            
        self.to_file(path, **kwargs)
            
            
class PlistDecoderMixin(FileStringMixin):
    
    ENCODER: Optional[PlistEncoder] = None
    DECODER: Optional[PlistDecoder] = None
    CONTAINER: Optional[str] = None
    ENCODER_KEY: Optional[int] = None
    IS_ARRAY: bool = False
    path: PathString
    
    
    def load_data(
            self,
            node:ET.Element, 
            is_array:Optional[bool]=None,
            encoder_key:Optional[int]=None,
            decoder:Optional[PlistEncoder]=None,
            container:Optional[int]=None,
            **kwargs
            ):
        
        cls = type(self)
        is_array = cls.IS_ARRAY if is_array is None else is_array
        encoder_key = cls.ENCODER_KEY if encoder_key is None else encoder_key
        decoder = cls.DECODER if decoder is None else decoder
        container = cls.CONTAINER if container is None else container
        data = self if container is None else getattr(self, container)
        
        try:
            validate_dict_node(node, is_array=is_array, encoder_key=encoder_key)
        except Exception as e:
            raise RuntimeError(f"[{type(self).__name__}] failed to validate node") from e
        
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
            is_array:Optional[bool]=None,
            encoder_key:Optional[int]=None,
            encoder:Optional=None,
            container:Optional[int]=None,
            **kwargs):
        
        cls = type(self)
        is_array = cls.IS_ARRAY if is_array is None else is_array
        encoder_key = cls.ENCODER_KEY if encoder_key is None else encoder_key
        encoder = cls.ENCODER if encoder is None else encoder
        container = cls.CONTAINER if container is None else container
        data = self if container is None else getattr(self, container)
        
        node = ET.Element("d")
        
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
    def from_node(cls, node:ET.Element, **kwargs):
        
        new = cls()
        
        try:
            new.load_data(node=node, **kwargs)
        except Exception as e:
            raise RuntimeError(f"[{cls.__name__}] failed to load node") from e
        return new
    
    def to_node(self, node:Optional[ET.Element]=None, **kwargs):
        
        try:
            result = self.save_data(**kwargs)
            
            if node is None:
                node = result
            else:
                node[:] = result[:]
        except Exception as e:
            raise RuntimeError(f"[{type(self).__name__}] failed to save node") from e
        return node
    
    
    @classmethod
    def from_string(cls, string:str, **kwargs):
        try:
            node = ET.fromstring(string)
            
            root = get_plist_root(node)
        except Exception as e:
            raise RuntimeError(f"[{cls.__name__}] failed to load string") from e
            
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
    
    
    def update_file(self, **kwargs):
        self.to_file(path=self.path, **kwargs)
        
        
    def reload_file(self, encoding="utf-8", **kwargs):
        
        try:
            with open(self.path, "r", encoding=encoding) as file:
                string = file.read()
            
            node = ET.fromstring(string)        
            root = get_plist_root(node)
        except Exception as e:
            raise RuntimeError(f"[{type(self).__name__}] failed to reload plist") from e
            
        self.load_data(node=root,**kwargs)


    def invoke(
            self, 
            method:str, 
            target:Optional[set]=None, 
            is_array:Optional[bool]=None, 
            **kwargs
            ):
        
        is_array = type(self).IS_ARRAY if is_array is None else is_array
        
        if is_array:
            items = enumerate(self)
            values = (v for i, v in items if target is None or i in target)
        else:
            items = self.items()
            values = (v for k, v in items if target is None or k in target)
        
        for value in values:
            value_method = getattr(value, method, None)
            if callable(value_method):
                value_method(**kwargs)


class DataclassDecoderMixin:
    
    ENCODER: Optional[StringDictEncoder] = staticmethod(dict_serializer)
    DECODER: Optional[StringDictDecoder] = None
    CONDITION: Optional[KeyValueCondition] = None
    FROM_ARRAY: bool = True
    SEPARATOR: str = ','
    MAX_SPLIT: Optional[int] = None
    
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
                f"[{cls.__name__}] expected at most {f_len} tokens, got {length}"
                )
        
        if from_array:            
            for field, token in zip(f, tokens):
                try:
                    key, value = decoder(field.name, token)
                except Exception as e:
                    raise ValueError(
                        f"[{cls.__name__}] failed to decode field '{field.name}'"
                        ) from e
                class_args[key] = value
        else:
            if length % 2 != 0:
                raise ValueError(
                    f"[{cls.__name__}] expected an even number of key-value tokens, got {length}"
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
                            f"[{cls.__name__}] failed to decode key / value pair {1+i//2}"
                            ) from e
                        
                if hasattr(cls, key):
                    class_args[key] = value
                else:
                    raise ValueError(
                        f"[{cls.__name__}] got unexpected field '{key}'"
                        )
        return cls(**class_args)
        
    
    def to_tokens(
            self,
            from_array:Optional[bool]=None,
            condition:Optional[Callable]=None,
            encoder:Optional[StringDictEncoder]=None
            ) -> Sequence[str]:
        
        cls = type(self)
        from_array = cls.FROM_ARRAY if from_array is None else from_array
        condition = cls.CONDITION if condition is None else condition
        encoder = cls.ENCODER if encoder is None else encoder
        
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
                        f"[{type(self).__name__}] failed to encode field '{key}'"
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
        
        separator = type(self).SEPARATOR if separator is None else separator
        
        parts = self.to_tokens(**kwargs)
        
        return separator.join(parts)


class DictDecoderMixin:
    
    ENCODER: Optional[StringDictEncoder] = staticmethod(dict_serializer)
    DECODER: Optional[StringDictDecoder] = None
    CONTAINER: Optional[str] = None
    CONDITION: Optional[KeyValueCondition] = None
    SEPARATOR: str = ','
    
    @classmethod
    def from_tokens(
            cls, 
            tokens:Sequence[str],
            decoder:Optional[StringDictDecoder]=None,
            container:Optional[str]=None
            ) -> Self:
        
        decoder = cls.DECODER if decoder is None else decoder
        container = cls.CONTAINER if container is None else container
        
        length = len(tokens)
        if length % 2 != 0:
            raise ValueError(
                f"[{cls.__name__}] expected an even number of key-value tokens, got {length}"
                )
            
        result = cls()
        data = result if container is None else getattr(result, container)
        
        it = iter(tokens)
        pairs = zip(it, it)
        # pairs = zip(tokens[::2], tokens[1::2])
        
        try:
            data.update(pairs if decoder is None else (decoder(k, v) for k, v in pairs))
        except Exception as e:
            raise ValueError(f"[{cls.__name__}] failed to decode") from e
        
        return result
    
    
    def to_tokens(
            self, 
            encoder:Optional[StringDictEncoder]=None,
            condition:Optional[KeyValueCondition]=None,
            container:Optional[str]=None
            ) -> Sequence[str]:
        
        cls = type(self)
        encoder = cls.ENCODER if encoder is None else encoder
        condition = cls.CONDITION if condition is None else condition
        container = cls.CONTAINER if container is None else container
        data = self if container is None else getattr(self, container)
            
        try:
            return [
                part
                for key, value in data.items()
                if condition is None or condition(key, value)
                for part in encoder(key, value)
            ]
        except Exception as e:
            raise ValueError(
                f"[{type(self).__name__}] failed to encode"
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
        separator = type(self).SEPARATOR if separator is None else separator
        
        parts = self.to_tokens(**kwargs)
        return separator.join(parts)


class ArrayDecoderMixin:
    
    ENCODER: Optional[StringEncoder] = staticmethod(serialize)
    DECODER: Optional[StringDecoder] = None
    CONTAINER: Optional[str] = None
    GROUP_SIZE: int = 1
    SEPARATOR: str = ','
    KEEP_SEPARATOR: bool = False
    
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
        data = result if container is None else getattr(result, container)
        
        try:
            if group_size > 1:
                for i in range(0, len(tokens), group_size):
                    data.append(decoder(tokens[i:i + group_size]) if decoder else tokens[i:i + group_size])
            elif decoder:
                data.extend(decoder(token) for token in tokens)
            else:
                data.extend(tokens)
        except Exception as e:
            raise ValueError(f"[{cls.__name__}] failed to decode") from e
                
        return result
    
    
    def to_tokens(
            self,
            encoder:Optional[StringEncoder]=None,
            group_size:Optional[int]=None,
            container:Optional[str]=None
            ) -> Sequence[str]:
        
        cls = type(self)
        encoder = cls.ENCODER if encoder is None else encoder
        group_size = cls.GROUP_SIZE if group_size is None else group_size
        container = cls.CONTAINER if container is None else container
        data = self if container is None else getattr(self, container)
        
        tokens = []
        try:
            if group_size > 1:
                for x in data:
                    group = encoder(x) if encoder else x
                    if len(group) != group_size:
                        raise ValueError(
                            f"[{type(self).__name__}] expected {group_size} tokens from encoder, got {len(group)}"
                            )
                    tokens.extend(group)
            elif encoder:
                tokens.extend(encoder(x) for x in data)
            else:
                tokens.extend(data)
                
        except Exception as e:
            raise ValueError(f"[{type(self).__name__}] failed to encode") from e
        
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
        
        cls = type(self)
        separator = cls.SEPARATOR if separator is None else separator        
        keep_separator = cls.KEEP_SEPARATOR if keep_separator is None else keep_separator
        separator = '' if keep_separator else separator
        
        tokens = self.to_tokens(**kwargs)
        
        return separator.join(tokens)


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
        
        if string:        
            start_delimiter = cls.START_DELIMITER if start_delimiter is None else start_delimiter
            end_delimiter = cls.END_DELIMITER if end_delimiter is None else end_delimiter
            
            if start_delimiter: 
                string = string.removeprefix(start_delimiter)
            
            if end_delimiter: 
                string = string.removesuffix(end_delimiter)
        
        return super().from_string(string, *args, **kwargs)
    
    
    def to_string(
            self,
            *args,
            start_delimiter:Optional[str]=None,
            end_delimiter:Optional[str]=None,
            **kwargs
            ) -> str:
        
        cls = type(self)
        start_delimiter = cls.START_DELIMITER if start_delimiter is None else start_delimiter
        end_delimiter = cls.END_DELIMITER if end_delimiter is None else end_delimiter
        
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
            compression_level:Optional[int]=None,
            **kwargs
            ) -> str:
        
        cls = type(self)
        compressed = cls.COMPRESSED if compressed is None else compressed
        compression = cls.COMPRESSION if compression is None else compression
        cypher = cls.CYPHER if cypher is None else cypher
        
        string = super().to_string(**kwargs)
        
        
        if compressed:
            kw = {}
            if compression_level is not None: kw["level"] = compression_level
                
            string = compress_string(string, compression=compression,xor_key=cypher,**kw)
        
        return string
    

class FilePathMixin:
    
    EXTENSION: Optional[str] = None
    
    def _name_fallback_(self):
        raise ValueError("[{type(self).__name__}] name fallback was not provided")
    
    @classmethod
    def from_file(
            cls, 
            path:PathString,
            extension:Optional[str]=None,
            **kwargs: Any
            ) -> Self:
        
        path = Path(path)
        extension = cls.EXTENSION if extension is None else extension
        path_ext = (path.suffix or "").removeprefix(".")
        
        if path.is_dir():
            raise ValueError(
                "expected file, got directory instead"
                )
        
        if extension is not None and path_ext != extension:
            raise ValueError(
                "file has invalid extension, expected '{extension}', got '{path_ext}' instead"
                )
            
        return super().from_file(path=path,**kwargs)
      
    
    def to_file(self, 
            path:Optional[PathString]=None, 
            extension:Optional[str]=None,
            **kwargs):
        
        path = Path(path or '.')
        extension = type(self).EXTENSION if extension is None else extension
        path_ext = (path.suffix or "").removeprefix(".")
                
        if not path_ext:
            if extension is None:
                raise ValueError(
                    "cannot resolve default filename as extension was not provided"
                    )
            name = self._name_fallback_()
            if name is None:
                raise ValueError(
                    "cannot resolve default filename as the name fallback returned None"
                    )
            path = (path / name).with_suffix('.' + extension)
            
        elif extension is not None and path_ext != extension:
            raise ValueError(
                "file has invalid extension, expected '{extension}', got '{path_ext}' instead"
                )
            
        super().to_file(path=path,**kwargs)
        

class LoadPlistContentMixin:
    
    SELECTORS: Optional[set] = None
    LOAD_CONTENT: bool = True
    SAVE_CONTENT: bool = True
    
    @classmethod
    def from_string(cls, string:str, load_content:Optional[bool]=None, content_selectors:Optional[set]=None, **kwargs):
        new = super().from_string(string, **kwargs)
        if load_content if load_content is not None else cls.LOAD_CONTENT:
            new.load(selectors=content_selectors)
            
        return new
    
    
    def to_string(self, save_content:Optional[bool]=None, content_selectors:Optional[set]=None, **kwargs):
        
        if save_content if save_content is not None else type(self).SAVE_CONTENT:
            self.save(selectors=content_selectors)
        
        return super().to_string(**kwargs)
        
        
    def load(self, selectors:Optional[set]=None,**kwargs):
        target = type(self).SELECTORS if selectors is None else selectors
        self.invoke("load",target=target,**kwargs)
        
            
    def save(self, selectors:Optional[set]=None,**kwargs):
        target = type(self).SELECTORS if selectors is None else selectors
        self.invoke("save",target=target,**kwargs)


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
        data = new if container is None else getattr(new, container)
        
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
        
        cls = type(self)
        encoder = cls.FOLDER_ENCODER if encoder is None else encoder
        container = cls.CONTAINER if container is None else container
        data = self if container is None else getattr(self, container)
            
        folder_path = Path(path)
        
        if not folder_path.is_dir():
            raise ValueError("provided path is not a directory.")
        
        for item in data:
            encoder(item, folder_path)
            