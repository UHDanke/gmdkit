# Imports
from typing import Any

# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.serialization.classes import DictField
from gmdkit.serialization.functions import kv_wrap, from_node_wrap, to_node_wrap
from gmdkit.serialization.type_cast import to_bool, from_bool
from gmdkit.serialization.mixins import PlistDecoderMixin
from gmdkit.serialization.type_cast import decode_text, encode_text


class PlistDict(PlistDecoderMixin,DictClass[str, Any]):
    pass

class PlistBoolDict(PlistDecoderMixin, DictClass[str, bool]):
    pass

class StrBoolDict(PlistDecoderMixin,DictClass[str,bool]):
    DECODER = staticmethod(kv_wrap(None, from_node_wrap(to_bool), None))
    ENCODER = staticmethod(kv_wrap(None, to_node_wrap(from_bool), None))

class IntBoolDict(PlistDecoderMixin,DictClass[int,bool]):
    DECODER = staticmethod(kv_wrap(int, from_node_wrap(to_bool), None))
    ENCODER = staticmethod(kv_wrap(str, to_node_wrap(from_bool), None))

class StrIntDict(PlistDecoderMixin,DictClass[str,int]):
    DECODER = staticmethod(kv_wrap(None, from_node_wrap(int), None))
    ENCODER = staticmethod(kv_wrap(None, to_node_wrap(str), None))

class IntStrDict(PlistDecoderMixin,DictClass[int,str]):
    DECODER = staticmethod(kv_wrap(int, str, None))
    ENCODER = staticmethod(kv_wrap(str, str, None))    

class IntIntDict(PlistDecoderMixin, DictClass[int, int]):
    DECODER = staticmethod(kv_wrap(int, from_node_wrap(int), None))
    ENCODER = staticmethod(kv_wrap(str, to_node_wrap(str), None))

class StrStrDict(PlistDecoderMixin, DictClass[str, str]):
    DECODER = staticmethod(kv_wrap(None, from_node_wrap(lambda s: s or ""), None))
    ENCODER = staticmethod(kv_wrap(None, to_node_wrap(str), None))

def bool_field(key:str) -> DictField:
    return DictField(key=key, decoder=to_bool, encoder=from_bool, default=False)

def int_field(key:str) -> DictField:
    return DictField(key=key, decoder=int, encoder=str, default=0)

def str_field(key:str) -> DictField:
    return DictField(key=key, decoder=lambda s: s or "", encoder=str, default="")

def encoded_field(key:str) -> DictField:
    return DictField(key=key, decoder=decode_text, encoder=encode_text, default="")

def node_field(key:str,cls) -> DictField:
    return DictField(key=key, default_factory=cls, decoder=cls.from_node, encoder=cls.to_node, is_node=True)

def serial_field(key:str,cls) -> DictField:
    return DictField(key=key, default_factory=cls, decoder=cls.from_string, encoder=cls.to_string)

def lazy_field(key:str,cls) -> DictField:
    return DictField(key=key, default_factory=cls, decoder=cls.load_string, encoder=cls.save_string)

def base64_field(key:str,cls) -> DictField:
    return DictField(key=key, default_factory=cls, decoder=cls.from_base64, encoder=cls.to_base64)