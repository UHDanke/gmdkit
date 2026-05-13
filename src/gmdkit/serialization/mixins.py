# Imports
from pathlib import Path
import xml.etree.ElementTree as ET
from contextlib import contextmanager
from typing import (
    Any, Self, Literal, 
    Optional, 
    Callable, Sequence,
    )

# Package Imports
from gmdkit.serialization.type_cast import (
    serialize, dict_serializer
)
from gmdkit.utils.typing import (
    PathString,
    StringDecoder, StringEncoder,
    StringDictDecoder, StringDictEncoder,
    KeyValueCondition,
    PlistDecoder,PlistEncoder,
    NumKey,
    MISSING
)
from gmdkit.serialization.functions import (
    decompress_string, compress_string,
    read_plist, write_plist,
    validate_dict_node, get_plist_root,
    get_fields, get_field_names, get_field_names_ordered
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


    @classmethod
    @contextmanager
    def open(cls, path: PathString, encoding="utf-8", **kwargs):
        instance = cls.from_file(path, encoding=encoding, **kwargs)
        try:
            yield instance
        except Exception:
            raise
        else:
            instance.to_file(path, encoding=encoding)


class DefaultPathMixin(FileStringMixin):
    
    DEFAULT_PATH: Optional[PathString] = None
    
    @classmethod
    def from_default_path(cls, **kwargs) -> Self:
        
        path = cls.DEFAULT_PATH
        
        if path is None:
            raise ValueError("[{cls.__name__}] default path does not exist")
        
        return cls.from_file(path,**kwargs)
    
    
    def to_default_path(self, **kwargs):
        cls = type(self)
        path = cls.DEFAULT_PATH
        
        if path is None:
            raise ValueError("[{cls.__name__}]  default path does not exist")
            
        self.to_file(path, **kwargs)
    
    
    @classmethod
    @contextmanager
    def open_default(cls, **kwargs):
        instance = cls.from_default_path(**kwargs)
        try:
            yield instance
        except Exception:
            raise
        else:
            instance.to_default_path(**kwargs)

            
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
            decoder:Optional[PlistEncoder]=None,
            container:Optional[int]=None,
            **kwargs
            ):
        
        cls = type(self)
        is_array = cls.IS_ARRAY
        encoder_key = cls.ENCODER_KEY
        decoder = cls.DECODER if decoder is None else decoder
        container = cls.CONTAINER if container is None else container
        data = self if container is None else getattr(self, container)
        
        try:
            validate_dict_node(node, is_array=is_array, encoder_key=encoder_key)
        except Exception as e:
            raise RuntimeError(f"[{cls.__name__}] failed to validate node") from e
        
        data.clear()
        
        start = 2 if is_array or encoder_key is not None else 0
        length = len(node)
        index_range = range(start, length, 2)
        use_kwargs = bool(kwargs)
    
        if decoder:
            if is_array:
                append_func = data.append
                if use_kwargs:
                    for i in index_range:
                        append_func(decoder(node[i + 1], **kwargs))
                else:
                    for i in index_range:
                        append_func(decoder(node[i + 1]))
            else:
                set_item = data.__setitem__
                if use_kwargs:
                    for i in index_range:
                        set_item(*decoder(node[i].text, node[i + 1], **kwargs))
                else:
                    for i in index_range:
                        set_item(*decoder(node[i].text, node[i + 1]))
        else:
            if is_array:
                append_func = data.append
                for i in index_range:
                    append_func(read_plist(node[i + 1]))
            else:
                set_item = data.__setitem__
                for i in index_range:
                    set_item(node[i].text, read_plist(node[i + 1]))

    
    def save_data(
            self,
            encoder:Optional=None,
            container:Optional[int]=None,
            **kwargs):
        
        cls = type(self)
        is_array = cls.IS_ARRAY
        encoder_key = cls.ENCODER_KEY
        encoder = cls.ENCODER if encoder is None else encoder
        container = cls.CONTAINER if container is None else container
        data = self if container is None else getattr(self, container)
        
        node = ET.Element("d")
        
        if is_array:
            ET.SubElement(node, 'k').text = '_isArr'
            ET.SubElement(node, 't')
            items = enumerate(data, start=1)
            write = (
                (lambda k, v: (f'k_{k}', encoder(v, **kwargs)))
                if encoder else
                (lambda k, v: (f'k_{k}', write_plist(v)))
            )
        else:
            if encoder_key is not None:
                ET.SubElement(node, 'k').text = 'kCEK'
                ET.SubElement(node, 'i').text = str(encoder_key)
            items = data.items()
            write = (
                (lambda k, v: encoder(k, v, **kwargs))
                if encoder else
                (lambda k, v: (k, write_plist(v)))
            )
    
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
            decoder:Optional[StringDictDecoder]=None,
            **kwargs
            ) -> Self:
        
        from_array = cls.FROM_ARRAY
        decoder = cls.DECODER if decoder is None else decoder
                
        f = get_fields(cls)
        length = len(tokens)
        f_len = len(f) if from_array else len(f) * 2

        if length > f_len:
            raise ValueError(
                f"[{cls.__name__}] expected at most {f_len} tokens, got {length}"
            )
        
        class_args = {}
    
        if from_array:
            if decoder is None:
                class_args = {field.name: token for field, token in zip(f, tokens)}
            else:
                class_args = {}
                for field, token in zip(f, tokens):
                    try:
                        key, value = decoder(field.name, token)
                    except Exception as e:
                        raise ValueError(
                            f"[{cls.__name__}] failed to decode field '{field.name}': '{token}'"
                        ) from e
                    class_args[key] = value
        else:
            if length % 2 != 0:
                raise ValueError(
                    f"[{cls.__name__}] expected an even number of key-value tokens, got {length}"
                )
            field_names = get_field_names(cls)
            it = iter(tokens)
    
            if decoder is None:
                for key, value in zip(it, it):              
                    if key not in field_names:
                        raise ValueError(f"[{cls.__name__}] got unexpected field '{key}'")
                    class_args[key] = value
            else:
                for raw_key, raw_value in zip(it, it):
                    try:
                        key, value = decoder(raw_key, raw_value)
                    except Exception as e:
                        raise ValueError(
                            f"[{cls.__name__}] failed to decode key '{raw_key}'"
                        ) from e
                    if key not in field_names:
                        raise ValueError(f"[{cls.__name__}] got unexpected field '{key}'")
                    class_args[key] = value
    
        return cls(**class_args)
    
    
    def to_tokens(
            self,
            condition:Optional[Callable]=None,
            encoder:Optional[StringDictEncoder]=None
            ) -> Sequence[str]:
        
        cls = type(self)
        from_array = cls.FROM_ARRAY
        condition = cls.CONDITION if condition is None else condition
        encoder = cls.ENCODER if encoder is None else encoder
        
        field_data = [(key, getattr(self, key)) for key in get_field_names_ordered(cls)]
        
        if condition is not None:
            if from_array:
                end = len(field_data)
                for key, value in reversed(field_data):
                    if condition(key, value):
                        end -= 1
                    else:
                        break
                field_data = field_data[:end]
            else:
                field_data = [(k, v) for k, v in field_data if not condition(k, v)]
                
        parts = []
        if encoder is None:
            for key, value in field_data:
                if not from_array:
                    parts.append(key)
                parts.append(value)
        else:
            for key, value in field_data:
                try:
                    ek, ev = encoder(key, value)
                except Exception as e:
                    raise ValueError(
                        f"[{cls.__name__}] failed to encode field '{key}'"
                    ) from e
                if not from_array:
                    parts.append(ek)
                parts.append(ev)
        
        return parts
    
        
    @classmethod
    def from_string(
            cls, 
            string:str,
            **kwargs
            ) -> Self:
        
        separator = cls.SEPARATOR
        max_split = cls.MAX_SPLIT
        
        if not string:
            return cls()
        
        if not separator:
            tokens = [*string[:max_split], string[max_split:]] if max_split is not None else list(string)
        else:
            tokens = string.split(separator, -1 if max_split is None else max_split)
        
        return cls.from_tokens(tokens,**kwargs)
            
        
    def to_string(self,**kwargs) -> str:
        return type(self).SEPARATOR.join(self.to_tokens(**kwargs))


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
        if decoder:
            try:
                for k, v in zip(it, it):
                    dk, dv = decoder(k, v)
                    data[dk] = dv
            except Exception as e:
                raise ValueError(f"[{cls.__name__}] failed to decode") from e
        else:
            data.update(zip(it, it))
        
        return result
    
    
    def to_tokens(
            self, 
            encoder:Optional[StringDictEncoder]=None,
            condition:Optional[KeyValueCondition]=None,
            container:Optional[str]=None,
            sort_keys:bool=False
            ) -> Sequence[str]:
        
        cls = type(self)
        encoder = cls.ENCODER if encoder is None else encoder
        condition = cls.CONDITION if condition is None else condition
        container = cls.CONTAINER if container is None else container
        data = self if container is None else getattr(self, container)
            
        result = []
        result_extend = result.extend
        items = data.items()
        if sort_keys:
            items = sorted(items)

        if encoder:
            try:
                for key, value in items:
                    if condition is None or condition(key, value):
                        result_extend(encoder(key, value))
            except Exception as e:
                raise ValueError(f"[{cls.__name__}] failed to encode") from e
        else:
            for key, value in data.items():
                if condition is None or condition(key, value):
                    result_extend((key, value))
    
        return result
                
            
    @classmethod
    def from_string(
            cls, 
            string:str,
            **kwargs,
            ) -> Self:
        
        separator = cls.SEPARATOR
        
        if string == "":
            return cls()
        
        tokens = list(string) if not separator else string.split(separator)
        
        return cls.from_tokens(tokens,**kwargs)
    
    
    def to_string(
            self,
            **kwargs
            ) -> str:
        return type(self).SEPARATOR.join(self.to_tokens(**kwargs))


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
            container:Optional[str]=None
            ) -> Self:
        
        decoder = cls.DECODER if decoder is None else decoder
        container = cls.CONTAINER if container is None else container
        group_size = cls.GROUP_SIZE
        
        result = cls()
        data = result if container is None else getattr(result, container)
        append = data.append
        extend = data.extend
        try:
            if group_size > 1:
                if len(tokens) % group_size != 0:
                    raise ValueError("token count not divisible by group size")
                for i in range(0, len(tokens), group_size):
                    append(decoder(tokens[i:i + group_size]) if decoder else tokens[i:i + group_size])
            elif decoder:
                extend(decoder(token) for token in tokens)
            else:
                extend(tokens)
        except Exception as e:
            raise ValueError(f"[{cls.__name__}] failed to decode") from e
                
        return result
    
    
    def to_tokens(
            self,
            encoder:Optional[StringEncoder]=None,
            container:Optional[str]=None
            ) -> Sequence[str]:
        
        cls = type(self)
        encoder = cls.ENCODER if encoder is None else encoder
        container = cls.CONTAINER if container is None else container
        data = self if container is None else getattr(self, container)
        group_size = cls.GROUP_SIZE
        
        try:
            if group_size > 1:
                tokens = []
                for x in data:
                    group = encoder(x) if encoder else x
                    if len(group) != group_size:
                        raise ValueError(
                            f"[{cls.__name__}] expected {group_size} tokens from encoder, got {len(group)}"
                            )
                    tokens.extend(group)
                return tokens
            elif encoder:
                return [encoder(x) for x in data]
            else:
                return list(data)
                
        except Exception as e:
            raise ValueError(f"[{cls.__name__}] failed to encode") from e
    
    
    @classmethod
    def from_string(
            cls, 
            string:str,
            **kwargs
            ) -> Self:
        
        separator = cls.SEPARATOR
        keep_separator = cls.KEEP_SEPARATOR
        
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
            **kwargs
            ) -> str:
        
        cls = type(self)
        separator = '' if cls.KEEP_SEPARATOR else cls.SEPARATOR
        
        tokens = self.to_tokens(**kwargs)
        
        return separator.join(tokens)


class DelimiterMixin:
    
    START_DELIMITER: Optional[str] = None
    END_DELIMITER: Optional[str] = None
    
    @classmethod
    def from_string(
            cls,
            string:str,
            **kwargs
            ) -> Self:
        
        if string:        
            start_delimiter = cls.START_DELIMITER
            end_delimiter = cls.END_DELIMITER
            
            if start_delimiter: 
                string = string.removeprefix(start_delimiter)
            
            if end_delimiter: 
                string = string.removesuffix(end_delimiter)
        
        return super().from_string(string, **kwargs)
    
    
    def to_string(
            self,
            **kwargs
            ) -> str:
        
        string = super().to_string(**kwargs)
        
        if not string:
            return string

        cls = type(self)
        start_delim = cls.START_DELIMITER
        end_delim = cls.END_DELIMITER

        if start_delim and end_delim:
            string = f"{start_delim}{string}{end_delim}"
        elif start_delim:
            string = f"{start_delim}{string}"
        elif end_delim:
            string = f"{string}{end_delim}"

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
            **kwargs
            ) -> Self:
        
        compressed = cls.COMPRESSED if compressed is None else compressed
        compression = cls.COMPRESSION
        cypher = cls.CYPHER
        
        if compressed:
            string = decompress_string(string, compression=compression, xor_key=cypher)
            
        return super().from_string(string, **kwargs)
    
    
    def to_string(
            self,
            compressed:Optional[bool]=None,
            compression_level:Optional[int]=None,
            **kwargs
            ) -> str:
        
        cls = type(self)
        compressed = cls.COMPRESSED if compressed is None else compressed
        compression = cls.COMPRESSION
        cypher = cls.CYPHER
        
        string = super().to_string(**kwargs)
        
        
        if compressed:
            kw = {}
            if compression_level is not None: kw["level"] = compression_level
                
            string = compress_string(string, compression=compression,xor_key=cypher,**kw)
        
        return string
    

class FilePathMixin(FileStringMixin):
    
    EXTENSION: Optional[str] = None
    
    def _name_fallback_(self):
        raise ValueError(f"[{type(self).__name__}] name fallback was not provided")
    
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
        

class PlistLoaderMixin(PlistDecoderMixin):
    
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
        
        if extension is None:
            raise ValueError("extension is None")
        
        new = cls()
        data = new if container is None else getattr(new, container)
        
        for file_path in Path(path).glob(f'*.{extension}'):
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


class DictDefaultsMixin:

    TYPES: Optional[dict[NumKey, Callable]] = None
    DEFAULTS: Optional[dict[NumKey, Any]] = None

    def setdefault(self, key, default=MISSING):
        cls = type(self)

        types = cls.TYPES or {}
        defaults = cls.DEFAULTS or {}

        if key not in self:

            if default is not MISSING:
                self[key] = default

            elif key in defaults:
                self[key] = defaults[key]

            elif key in types:
                self[key] = types[key]()

        return self.get(key)

    def autodefaults(self, *keys, override:bool=False):
        cls = type(self)

        types = cls.TYPES or {}
        defaults = cls.DEFAULTS or {}

        if not keys:
            keys = tuple(set(types) | set(defaults))

        for key in keys:

            if not override and key in self:
                continue

            if key in defaults:
                self[key] = defaults[key]

            elif key in types:
                self[key] = types[key]()

    def cleardefaults(self, *keys):
        cls = type(self)

        types = cls.TYPES or {}
        defaults = cls.DEFAULTS or {}

        if not keys:
            keys = tuple(set(types) | set(defaults))

        for key in keys:
            self.pop(key, None)