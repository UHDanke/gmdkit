# Imports
from typing import Callable, Any, Optional
from collections import ChainMap

# Package Imports
from gmdkit.utils.typing import MISSING
from gmdkit.serialization.functions import (
    read_plist, write_plist,
    )


class Codec:
    """Base codec: calls function directly on the value. This is the
    behavior for node-level fields (is_node=True) - no unwrapping/wrapping."""

    __slots__ = ("function", "allow_kwargs")

    def __init__(self, function: Callable, allow_kwargs: bool = False):
        self.function = function
        self.allow_kwargs = allow_kwargs

    def __call__(self, value, **kwargs):
        if self.allow_kwargs:
            return self.function(value, **kwargs)
        return self.function(value)


class DecoderCodec(Codec):
    """Extracts node.text before delegating to the wrapped function."""

    def __call__(self, node, **kwargs):
        return super().__call__(node.text, **kwargs)


class EncoderCodec(Codec):
    """Delegates to the wrapped function, then plist-wraps the result."""

    def __call__(self, value, **kwargs):
        result = super().__call__(value, **kwargs)
        return write_plist(result)


def codec_cast(
    codecs,
    *,
    key_start=None,
    key_end=None,
    default=None,
):
    c_get = codecs.get
    has_default = callable(default)
    use_start = callable(key_start)
    use_end = callable(key_end)

    def cast_func(key, value, **kwargs):
        if use_start:
            key = key_start(key)

        codec = c_get(key)
        if codec is None:
            value = default(value) if has_default else value
        else:
            value = codec(value, **kwargs)

        if use_end:
            key = key_end(key)

        return key, value

    return cast_func


class FieldMetaclass(type):
    KEY_DECODER: Optional[Callable] = None
    KEY_ENCODER: Optional[Callable] = None

    DEFAULT_DECODER = staticmethod(read_plist)
    DEFAULT_ENCODER = staticmethod(write_plist)

    DECODER: Callable
    ENCODER: Callable

    _ENCODER_MAP: dict
    _DECODER_MAP: dict
    _KEYS: set
    _ENCODER_CHAIN: ChainMap
    _DECODER_CHAIN: ChainMap
    _KEY_CHAIN: ChainMap

    def add_field(
        cls,
        key,
        *,
        encoder: Callable = None,
        decoder: Callable = None,
        is_node: bool = False,
        pass_kwargs: bool = False,
    ):
        if "_KEYS" not in cls.__dict__:
            cls._KEYS = set()
            
        if key in cls._KEYS:
            raise RuntimeError(f"a field with key '{key}' already exists")
        
        cls._KEYS.add(key)
        
        if encoder is not None:
            if "_ENCODER_MAP" not in cls.__dict__:
                cls._ENCODER_MAP = {}
            codec_cls = Codec if is_node else EncoderCodec
            cls._ENCODER_MAP[key] = codec_cls(
                encoder,
                allow_kwargs=pass_kwargs,
            )

        if decoder is not None:
            if "_DECODER_MAP" not in cls.__dict__:
                cls._DECODER_MAP = {}
            codec_cls = Codec if is_node else DecoderCodec
            cls._DECODER_MAP[key] = codec_cls(
                decoder,
                allow_kwargs=pass_kwargs,
            )

    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)

        cls._DECODER_MAP = cls.__dict__.get("_DECODER_MAP", {})
        cls._ENCODER_MAP = cls.__dict__.get("_ENCODER_MAP", {})
        cls._KEYS = cls.__dict__.get("_KEYS", {})

        cls._DECODER_CHAIN = ChainMap(*(
            klass.__dict__["_DECODER_MAP"]
            for klass in cls.__mro__
            if "_DECODER_MAP" in klass.__dict__
        ))

        cls._ENCODER_CHAIN = ChainMap(*(
            klass.__dict__["_ENCODER_MAP"]
            for klass in cls.__mro__
            if "_ENCODER_MAP" in klass.__dict__
        ))
        
        cls._KEY_CHAIN = ChainMap(*(
            klass.__dict__["_KEYS"]
            for klass in cls.__mro__
            if "_KEYS" in klass.__dict__
        ))
        
        cls.DECODER = staticmethod(
            codec_cast(
                cls._DECODER_CHAIN,
                default=cls.DEFAULT_DECODER,
                key_start=cls.KEY_DECODER,
            )
        )

        cls.ENCODER = staticmethod(
            codec_cast(
                cls._ENCODER_CHAIN,
                default=cls.DEFAULT_ENCODER,
                key_end=cls.KEY_ENCODER,
            )
        )

        return cls

    def get_decoders(self):
        return {k: v.function for k,v in self._DECODER_CHAIN.items()}
    
    def get_encoders(self):
        return {k: v.function for k,v in self._ENCODER_CHAIN.items()}
    
    def get_keys(self):
        return set(self._KEY_CHAIN)
    

class DictField:
    key: str
    default: Any
    default_factory: Callable
    encoder: Callable | None
    decoder: Callable | None
    is_node: bool
    pass_kwargs: bool
    _class_container: str | None

    def __init__(self, key=None, default=MISSING, default_factory=None,
                 encoder=None, decoder=None, is_node=False, pass_kwargs=False):
        if default is not MISSING and default_factory is not None:
            raise ValueError("Cannot specify both 'default' and 'default_factory'")
        self.key = key
        self.default = default
        self.default_factory = default_factory
        self.encoder = encoder
        self.decoder = decoder
        self.is_node = is_node
        self.pass_kwargs = pass_kwargs
        self._class_container = None

    def __set_name__(self, owner, name):
        self.name = name
        if self.key is None:
            self.key = name
        self._class_container = getattr(owner, "CONTAINER", None)
        owner.add_field(
            self.key,
            encoder=self.encoder,
            decoder=self.decoder,
            is_node=self.is_node,
            pass_kwargs=self.pass_kwargs,
        )

    def _target(self, instance):
        if self._class_container is not None:
            return getattr(instance, self._class_container)
        return instance

    def __get__(self, instance, owner):
        if instance is None:
            return self
        target = self._target(instance)
        try:
            return target[self.key]
        except KeyError:
            if self.default_factory is not None:
                value = self.default_factory()
                target[self.key] = value
                return value
            if self.default is not MISSING:
                return self.default
            return None

    def __set__(self, instance, value):
        self._target(instance)[self.key] = value

    def __delete__(self, instance):
        del self._target(instance)[self.key]
