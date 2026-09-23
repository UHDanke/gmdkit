# Imports
from typing import Any

# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.serialization.functions import kv_wrap, from_node_wrap, to_node_wrap
from gmdkit.serialization.type_cast import to_bool, from_bool
from gmdkit.serialization.mixins import PlistDecoderMixin


class StrBoolDict(PlistDecoderMixin,DictClass[str,bool]):
    DECODER = staticmethod(kv_wrap(None, from_node_wrap(to_bool), None))
    ENCODER = staticmethod(kv_wrap(None, to_node_wrap(from_bool), None))


class IntBoolDict(PlistDecoderMixin,DictClass[int,bool]):
    DECODER = staticmethod(kv_wrap(int, from_node_wrap(to_bool), None))
    ENCODER = staticmethod(kv_wrap(str, to_node_wrap(from_bool), None))


class PlistDict(PlistDecoderMixin,DictClass[str, Any]):
    pass
    #DECODER = staticmethod(kv_wrap(None, None, None))
    #ENCODER = staticmethod(kv_wrap(None, None, None))

class StrIntDict(PlistDecoderMixin,DictClass[str,int]):
    DECODER = staticmethod(kv_wrap(str, int, None))
    ENCODER = staticmethod(kv_wrap(str, str, None))


class IntStrDict(PlistDecoderMixin,DictClass[int,str]):
    DECODER = staticmethod(kv_wrap(int, str, None))
    ENCODER = staticmethod(kv_wrap(str, str, None))
