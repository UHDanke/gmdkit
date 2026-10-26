# Imports
from typing import Callable, Literal, Optional, Any, get_type_hints, TypeVar, overload
import numpy as np
from dataclasses import field, fields, dataclass, MISSING, Field
import sys
import xml.etree.ElementTree as ET
import base64
import zlib
import gzip
from enum import Enum

# Package Imports
from gmdkit.serialization.type_cast import (
    from_float, from_bool, to_bool, dict_cast
    )
from gmdkit.utils.typing import (
    StringDictDecoder,
    StringDictEncoder,
    PathString,
    Element
    )
from gmdkit.utils.functions import typed_cache

@typed_cache(maxsize=256)
def get_fields(cls) -> tuple[Field, ...]:
    return tuple(f for f in fields(cls) if not f.name.startswith("_"))

@typed_cache(maxsize=256)
def get_field_names(cls) -> set[str]:
    return {f.name for f in get_fields(cls)}

@typed_cache(maxsize=256)
def get_field_names_ordered(cls) -> tuple[str, ...]:
    return tuple(f.name for f in get_fields(cls))

@typed_cache(maxsize=256)
def has_field(cls, key: str) -> bool:
    return key in get_field_names(cls)

def set_field(obj, key: str, value) -> None:
    if not has_field(type(obj), key):
        raise KeyError(key)
    setattr(obj, key, value)

def get_field(obj, key: str):
    if not has_field(type(obj), key):
        raise KeyError(key)
    return getattr(obj, key)

def xor(data: bytes, key: bytes) -> bytes:
    d = np.frombuffer(data, dtype=np.uint8)
    k = np.frombuffer(key * (len(data) // len(key) + 1), dtype=np.uint8)[:len(data)]
    return (d ^ k).tobytes()


def decompress_string(
        string:str,
        xor_key:Optional[bytes]=None,
        compression:Optional[Literal["zlib","gzip","deflate","auto"]]="auto",
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
            raise ValueError(f"unsupported decompression method: {compression}")

    return byte_stream.decode("utf-8",errors="ignore")


def compress_string(
        string:str,
        xor_key:Optional[bytes]=None,
        compression:Optional[Literal["zlib","gzip","deflate"]]="gzip",
        level:int=6
        ) -> str:

    byte_stream = string.encode()

    match compression:
        case 'zlib':
            byte_stream = zlib.compress(byte_stream, wbits=zlib.MAX_WBITS, level=level)
        case 'gzip':
            byte_stream = gzip.compress(byte_stream, compresslevel=level, mtime=0)
        case 'deflate':
            byte_stream = zlib.compress(byte_stream, wbits=-zlib.MAX_WBITS, level=level)
        case None:
            pass
        case _:
            raise ValueError(f"unsupported compression method: {compression}")

    byte_stream = base64.urlsafe_b64encode(byte_stream)

    if xor_key is not None:
        byte_stream = xor(byte_stream, key=xor_key)

    return byte_stream.decode()


def read_plist(node:Element) -> int|bool|float|str|dict|list:

    match node.tag:
        case 'i':
            return int(node.text)
        case 'r':
            return float(node.text)
        case 's':
            return node.text or ""
        case 't':
            return True
        case 'd'|'dict':
            num = len(node)

            if num == 0:
                return {}

            if (
                    num >= 2 and
                    node[0].tag == "k" and
                    node[0].text == "_isArr" and
                    node[1].tag == "t"
                    ):
                return [read_plist(node[i]) for i in range(3, len(node), 2)]

            return {
                node[i].text: read_plist(node[i + 1])
                for i in range(0, len(node) - 1, 2)
            }
        case _:
            raise ValueError(f"unknown node tag: {node.tag} for node {node}")


def write_plist(value:Any) -> Element:

    if isinstance(value, bool):
        if value:
            return Element("t")
        return None

    elif isinstance(value, int):
        node = Element("i")
        node.text = str(value)
        return node

    elif isinstance(value, float):
        node = Element("r")
        node.text = from_float(value)
        return node

    elif isinstance(value, str):
        node = Element("s")
        node.text = value
        return node

    elif isinstance(value, dict):
        root = Element("d")

        for k, v in value.items():
            node = write_plist(v)
            if node is None:
                continue
            ET.SubElement(root, "k").text = str(k)
            root.append(node)

        return root

    elif isinstance(value, (list, tuple)):
        root = Element("d")
        ET.SubElement(root, "k").text = "_isArr"
        root.append(Element("t"))

        for k, v in enumerate(value, start=1):
            node = write_plist(v)
            if node is None:
                continue
            ET.SubElement(root, "k").text = f"k_{k}"
            root.append(node)

        return root

    else:
        raise ValueError(f"class {type(value)} is not serializable")


def validate_dict_node(node:ET.Element, is_array:bool=False, encoder_key:Optional[int]=None):

    if node.tag not in ['d', 'dict']:
        raise ValueError("element is not a plist dict element")

    length = len(node)

    if length % 2 != 0:
        raise ValueError(f"expected an even number of key-value dict elements, got {length}")

    if length < 2:
        if is_array:
            raise ValueError(f"expected at least 2 header elements for array, found {length}")
        elif encoder_key is not None:
            raise ValueError(f"expected at least 2 header elements for encoded dict, found {length}")
        else:
            return

    key_el = node[0]
    val_el = node[1]

    array_header = key_el.tag == 'k' and key_el.text in ['_isArr','_IsArr'] and val_el.tag == 't' and val_el.text is None
    encoder_header = key_el.tag == 'k' and key_el.text == 'kCEK' and val_el.tag == 'i' and val_el.text is not None

    if is_array:
        if not array_header:
            raise ValueError(
                f"malformed array header, expected '<k>_isArr</k><t />', got '{ET.tostring(key_el).decode()}{ET.tostring(val_el).decode()}'"
                )
    elif encoder_key is not None:
        if not encoder_header:
            raise ValueError(
                f"malformed encoded struct header, expected '<k>kCEK</k><i>{encoder_key}</i>', got '{ET.tostring(key_el).decode()}{ET.tostring(val_el).decode()}'"
                )
        elif val_el.text != str(encoder_key):
            raise ValueError(f"encoder key does not match, expected '{encoder_key}', got '{val_el.text}'")
    elif array_header:
        raise ValueError("expected plain dict, found array header")
    elif encoder_header:
        raise ValueError("expected plain dict, found encoded dict header")

    for i in range(0, length, 2):
        if node[i].tag != 'k':
            raise ValueError(f"expected key tag 'k' at index {i}, got '{node[i].tag}'")


def get_plist_root(node:ET.Element) -> ET.Element:
    if node.tag != "plist":
        raise ValueError(f"expected root node to be <plist>, got <{node.tag}> instead")

    root = node.find("dict")

    if root is None:
        raise ValueError("plist does not contain a <dict> sub-element")

    return root


def from_plist_string(string: str) -> dict:
    tree = ET.fromstring(string)
    return read_plist(tree.find("dict"))


def to_plist_string(data:[dict,list]) -> str:
    root = ET.Element("plist", version="1.0", gjver="2.0")
    node = write_plist(data)
    node.tag = "dict"
    root.append(node)
    return ET.tostring(root, encoding='unicode')


def from_plist_file(path: PathString) -> dict:
    tree = ET.parse(path)
    root = tree.getroot()
    return read_plist(root.find("dict"))


def to_plist_file(data: Any, path: PathString):
    root = ET.Element("plist", version="1.0", gjver="2.0")
    node = write_plist(data)
    node.tag = "dict"
    root.append(node)
    tree = ET.ElementTree(root)
    tree.write(path, xml_declaration=True)


def decoder_from_type(type_hint:Any):

    if type_hint is bool:
        return to_bool

    if callable(type_hint):
        return type_hint

    raise ValueError(f"unsupported type hint: {type_hint}")


def encoder_from_type(type_hint:Any):

    if type_hint is bool:
        return from_bool

    if type_hint is float:
        return from_float

    if isinstance(type_hint, type) and issubclass(type_hint, (int, str)):
        return str

    if isinstance(type_hint, type) and issubclass(type_hint, Enum):
        return lambda x: str(x.value)

    raise ValueError(f"unsupported type hint: {type_hint}")


_T = TypeVar("_T")

@overload
def dataclass_decoder(
    cls: type[_T],
    *,
    decoder: Optional[StringDictDecoder] = ...,
    encoder: Optional[StringDictEncoder] = ...,
    condition: Optional[Callable] = ...,
    separator: Optional[str] = ...,
    from_array: Optional[bool] = ...,
    pair_separator: Optional[str] = ...,
    single_split: Optional[bool] = ...,
    max_split: Optional[int] = ...,
    auto_key: Optional[Callable] = ...,
    default_optional: bool = ...,
    default_kwargs: bool = ...,
    **kwargs,
) -> type[_T]: ...
 
 
@overload
def dataclass_decoder(
    cls: None = None,
    *,
    decoder: Optional[StringDictDecoder] = ...,
    encoder: Optional[StringDictEncoder] = ...,
    condition: Optional[Callable] = ...,
    separator: Optional[str] = ...,
    from_array: Optional[bool] = ...,
    pair_separator: Optional[str] = ...,
    single_split: Optional[bool] = ...,
    max_split: Optional[int] = ...,
    auto_key: Optional[Callable] = ...,
    default_optional: bool = ...,
    default_kwargs: bool = ...,
    **kwargs,
) -> Callable[[type[_T]], type[_T]]: ...
 
 
def dataclass_decoder(
        cls=None,
        decoder:Optional[StringDictDecoder]=None,
        encoder:Optional[StringDictEncoder]=None,
        condition:Optional[Callable]=None,
        separator:Optional[str]=None,
        from_array:Optional[bool]=None,
        pair_separator:Optional[str]=None,
        single_split:Optional[bool]=None,
        max_split:Optional[int]=None,
        auto_key: Optional[Callable] = None,
        default_optional: bool = False,
        default_kwargs: bool = False,
        *args,
        **kwargs
        ):
 
    def wrap(cls):
        cls = dataclass(cls, *args, **kwargs)
        hints = get_type_hints(cls, globalns=vars(sys.modules[cls.__module__]))
 
        if separator is not None:
            cls.SEPARATOR = separator
 
        if from_array is not None:
            cls.FROM_ARRAY = from_array
 
        if pair_separator is not None:
            cls.PAIR_SEPARATOR = pair_separator
 
        if single_split is not None:
            cls.SINGLE_SPLIT = single_split
 
        if max_split is not None:
            cls.MAX_SPLIT = max_split
 
        if getattr(cls, "PAIR_SEPARATOR", None):
            if getattr(cls, "FROM_ARRAY", True):
                raise TypeError(f"{cls.__name__}: pair_separator requires from_array=False")
            if getattr(cls, "MAX_SPLIT", None) is not None and not getattr(cls, "SINGLE_SPLIT", False):
                raise TypeError(f"{cls.__name__}: pair_separator with max_split requires single_split=True")
            if cls.PAIR_SEPARATOR == getattr(cls, "SEPARATOR", None):
                raise TypeError(f"{cls.__name__}: pair_separator must differ from separator")
 
        dkey_dict = {}
        ekey_dict = {}
        cond_dict = {}
        decoders = {}
        encoders = {}
        has_kwargs = set()
 
        fields = get_fields(cls)
        stream_fields = []
        for i, f in enumerate(fields,start=1):
            meta = f.metadata
            name = f.name
            key = meta.get("key")
            if key is None and auto_key is not None:
                key = auto_key(i)
 
            ft = hints[f.name]
 
            if key is not None and name != key:
                if key in dkey_dict:
                    raise ValueError(f"duplicate serialization key: {key!r}")
                dkey_dict[key] = name
                ekey_dict[name] = key
 
            group_size = meta.get("group_size", 1)

            if meta.get("use_streams"):
                if meta.get("decoder") is None or meta.get("encoder") is None:
                    raise ValueError(f"{cls.__name__}.{name}: use_streams needs a decoder and an encoder")
                if group_size != 1:
                    raise ValueError(f"{cls.__name__}.{name}: use_streams fields take no group_size")
                if not getattr(cls, "FROM_ARRAY", True):
                    raise ValueError(f"{cls.__name__}.{name}: use_streams needs the array form")
                stream_fields.append((meta["decoder"], meta["encoder"]))
                decoders[name] = str
                encoders[name] = str
            else:
                stream_fields.append(None)

                if group_size != 1 and not (isinstance(group_size, int) and group_size > 1):
                    raise ValueError(f"{cls.__name__}.{name}: group_size must be an int above 0")
                if group_size > 1 and not getattr(cls, "FROM_ARRAY", True):
                    raise ValueError(f"{cls.__name__}.{name}: group_size needs the array form")

                if group_size > 1:
                    decoders[name] = meta.get("decoder") or getattr(ft, "from_tokens", None)
                    encoders[name] = meta.get("encoder") or getattr(ft, "to_tokens", None)
                    if decoders[name] is None or encoders[name] is None:
                        raise ValueError(
                            f"{cls.__name__}.{name}: group_size {group_size} needs a decoder / encoder "
                            "taking / returning a list of tokens"
                        )
                else:
                    decoders[name] = meta.get("decoder") or decoder_from_type(ft)
                    encoders[name] = meta.get("encoder") or encoder_from_type(ft)


            allow_kwargs = meta.get("allow_kwargs")
            allow_kwargs = default_kwargs if allow_kwargs is None else allow_kwargs
 
            if allow_kwargs:
                has_kwargs.add(name)
 
            optional = meta.get("optional")
            optional = default_optional if optional is None else optional
 
            if optional:
                if f.default_factory is not MISSING:
                    default = f.default_factory()
                elif f.default is not MISSING:
                    default = f.default
                else:
                    default = None
                cond_dict[name] = default
 
        group_sizes = tuple(f.metadata.get("group_size", 1) for f in fields)
        cls.GROUP_SIZES = group_sizes
        cls.GROUPED = any(size != 1 for size in group_sizes)
        cls.STREAM_FIELDS = tuple(stream_fields) if any(c is not None for c in stream_fields) else ()

        cls.DECODER = staticmethod(
            decoder or dict_cast(
                decoders,
                key_start=dkey_dict.get if dkey_dict else None,
                allow_kwargs=has_kwargs
                )
            )
 
        cls.ENCODER = staticmethod(
            encoder or dict_cast(
                encoders,
                key_end=ekey_dict.get if ekey_dict else None,
                allow_kwargs=has_kwargs
        		)
            )
 
        if cond_dict:
            def is_default(key, value):
                return key in cond_dict and cond_dict[key] == value
        else:
            is_default = None
 
        cls.CONDITION = staticmethod(condition or is_default)
 
        return cls
 
    return wrap if cls is None else wrap(cls)


def field_decoder(
        *args,
        key:Optional[str]=None,
        decoder:Optional[Callable]=None,
        encoder:Optional[Callable]=None,
        optional:Optional[bool]=None,
        allow_kwargs:Optional[bool]=None,
        group_size:Optional[int]=None,
        use_streams:Optional[bool]=None,
        **kwargs
        ):

    d = dict(kwargs)

    original_md = d.get("metadata")
    if original_md is not None and not isinstance(original_md, dict):
        raise TypeError(f"'metadata' must be a dict if provided, got {type(original_md).__name__}")

    md = dict(original_md) if original_md else {}

    if "decoder" not in md and decoder is not None:
        md["decoder"] = decoder

    if "encoder" not in md and encoder is not None:
        md["encoder"] = encoder

    if "key" not in md and key is not None:
        md["key"] = key

    if "optional" not in md and optional is not None:
            md["optional"] = optional

    if "allow_kwargs" not in md and allow_kwargs is not None:
        md["allow_kwargs"] = allow_kwargs

    if "group_size" not in md and group_size is not None:
        md["group_size"] = group_size

    if "use_streams" not in md and use_streams is not None:
        md["use_streams"] = use_streams

    if md:
        d["metadata"] = md
    elif "metadata" in d:
        d.pop("metadata")

    return field(*args, **d)

def pass_kwargs(**kwargs):
    return kwargs

def kv_wrap(
        key_func: Optional[Callable[[Any], Any]] = None,
        value_func: Optional[Callable[..., Any]] = None,
        kwarg_handler: Optional[Callable[..., dict[str, Any]]] = pass_kwargs,
        ) -> Callable:

    def wrap(key, value, **kwargs) -> tuple:
        processed_kwargs = kwarg_handler(**kwargs) if kwarg_handler is not None else {}
        return (
            key_func(key) if key_func is not None else key,
            value_func(value, **processed_kwargs) if value_func is not None else value,
        )

    return wrap


def args_wrap(
        func: Callable[..., Any],
        max_args: Optional[int] = None,
        kwarg_handler: Optional[Callable[[dict[str, Any]], dict[str, Any]]] = pass_kwargs,
        ) -> Callable:

    def wrap(*args, **kwargs) -> Any:
        return func(
            *(args[:max_args] if max_args is not None else args),
           **(kwarg_handler(**kwargs) if kwarg_handler is not None else {}),
        )

    return wrap


def get_load_keys(func_dict:dict[Callable]) -> set:
    return {k for k, v in func_dict.items() if hasattr(v, "load") and hasattr(v, "save")}


def from_node_wrap(function:Callable):
    def get_node_text(node, **kwargs):
        return function(node.text, **kwargs)

    return get_node_text


def to_node_wrap(function:Callable):
    def return_node(value, **kwargs):
        string = function(value, **kwargs)
        return write_plist(string)

    return return_node


def from_node_dict(functions:dict[str,Callable],exclude:Optional[dict[str,bool]]=None):

    d = {}

    for k, f in functions.items():
        if exclude and k in exclude:
            d[k] = f
        else:
            d[k] = from_node_wrap(f)

    return d


def to_node_dict(functions:dict[str,Callable],exclude:Optional[dict[str,bool]]=None):

    d = {}

    for k, f in functions.items():
        if exclude and k in exclude:
            d[k] = f
        else:
            d[k] = to_node_wrap(f)

    return d


def codec_cast(
    codecs,
    *,
    key_start=None,
    key_end=None,
    default=None,
    prefixes=None,
):
    c_get = codecs.get
    has_default = callable(default)
    use_start = callable(key_start)
    use_end = callable(key_end)
    prefix_codecs = tuple(sorted(prefixes.items(), key=lambda item: -len(item[0]))) if prefixes else ()

    def cast_func(key, value, **kwargs):
        if use_start:
            key = key_start(key)

        codec = c_get(key)
        if codec is None and prefix_codecs and isinstance(key, str):
            for prefix, prefix_codec in prefix_codecs:
                if key.startswith(prefix):
                    codec = prefix_codec
                    break

        if codec is None:
            value = default(value) if has_default else value
        else:
            value = codec(value, **kwargs)

        if use_end:
            key = key_end(key)

        return key, value

    return cast_func