# Imports
from typing import Callable, Any, Optional, TypeVar, overload
from collections import ChainMap

# Package Imports
from gmdkit.utils.typing import MISSING
from gmdkit.serialization.functions import (
    read_plist, write_plist,
    )


V = TypeVar("V", bound="BaseInterface")


class Codec:

    __slots__ = ("function", "allow_kwargs")

    def __init__(self, function: Callable, allow_kwargs: bool = False):
        self.function = function
        self.allow_kwargs = allow_kwargs

    def __call__(self, value, **kwargs):
        if self.allow_kwargs:
            return self.function(value, **kwargs)
        return self.function(value)


class DecoderCodec(Codec):

    def __call__(self, node, **kwargs):
        return super().__call__(node.text, **kwargs)


class EncoderCodec(Codec):

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


class AliasField:
    def __init__(self, canonical: str = None):
        self.canonical = canonical

    def __set_name__(self, owner, name):
        self.name = name
        if self.canonical is None:
            self.canonical = name
        if "_ALIASES" not in owner.__dict__:
            owner._ALIASES = {}
        owner._ALIASES[name] = self.canonical
        self._container = getattr(owner, "CONTAINER", None)

    def _target(self, instance):
        if self._container is not None:
            return getattr(instance, self._container)
        return instance

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._target(instance)[self.canonical]

    def __set__(self, instance, value):
        self._target(instance)[self.canonical] = value

    def __delete__(self, instance):
        del self._target(instance)[self.canonical]


class DictField(AliasField):
    def __init__(self, key=None, default=MISSING, default_factory=None,
                 encoder=None, decoder=None, is_node=False, pass_kwargs=False):
        super().__init__(key)
        self.default = default
        self.default_factory = default_factory
        self.encoder = encoder
        self.decoder = decoder
        self.is_node = is_node
        self.pass_kwargs = pass_kwargs

    def __set_name__(self, owner, name):
        super().__set_name__(owner, name)
        owner.add_field(
            self.canonical,
            encoder=self.encoder,
            decoder=self.decoder,
            is_node=self.is_node,
            pass_kwargs=self.pass_kwargs,
        )

    def __get__(self, instance, owner):
        if instance is None:
            return self
        try:
            return self._target(instance)[self.canonical]
        except KeyError:
            if self.default_factory is not None:
                value = self.default_factory()
                self._target(instance)[self.canonical] = value
                return value
            if self.default is not MISSING:
                return self.default
            return None


class BaseInterface:
    CONTAINER = "obj"

    def __init__(self, obj: "FieldInterface"):
        self.obj = obj

    def __getattr__(self, name: str) -> Any:
        return getattr(self.obj, name)

    def __getitem__(self, key): return self.obj[key]
    def __setitem__(self, key, value): self.obj[key] = value
    def __delitem__(self, key): del self.obj[key]
    def __contains__(self, key): return key in self.obj
    def __len__(self): return len(self.obj)
    def __iter__(self): return iter(self.obj)
    def __repr__(self): return f"{type(self).__name__}({self.obj!r})"


class FieldMetaclass(type):
    KEY_DECODER: Optional[Callable] = None
    KEY_ENCODER: Optional[Callable] = None

    DEFAULT_DECODER: Callable = staticmethod(read_plist)
    DEFAULT_ENCODER: Callable = staticmethod(write_plist)

    DECODER: Callable
    ENCODER: Callable

    ID_KEY: Optional[str] = None

    _ENCODER_MAP: dict
    _DECODER_MAP: dict
    _KEYS: set
    _VIEW_REGISTRY: dict
    _ID_REGISTRY: dict
    _ENCODER_CHAIN: ChainMap
    _DECODER_CHAIN: ChainMap
    _KEY_CHAIN: ChainMap
    _VIEW_CHAIN: ChainMap
    _ID_CHAIN: ChainMap

    def add_field(cls, key, *, encoder=None, decoder=None, is_node=False, pass_kwargs=False):
        if "_KEYS" not in cls.__dict__:
            cls._KEYS = set()
        if key in cls._KEYS:
            raise RuntimeError(f"a field with key '{key}' already exists")
        cls._KEYS.add(key)
        if encoder is not None:
            if "_ENCODER_MAP" not in cls.__dict__:
                cls._ENCODER_MAP = {}
            codec_cls = Codec if is_node else EncoderCodec
            cls._ENCODER_MAP[key] = codec_cls(encoder, allow_kwargs=pass_kwargs)
        if decoder is not None:
            if "_DECODER_MAP" not in cls.__dict__:
                cls._DECODER_MAP = {}
            codec_cls = Codec if is_node else DecoderCodec
            cls._DECODER_MAP[key] = codec_cls(decoder, allow_kwargs=pass_kwargs)

    def register_id(cls, id_value, schema: type):
        if not issubclass(schema, BaseInterface):
            raise TypeError(f"{schema.__name__} must subclass BaseInterface")
        if "_VIEW_REGISTRY" not in cls.__dict__:
            cls._VIEW_REGISTRY = {}
        if "_ID_REGISTRY" not in cls.__dict__:
            cls._ID_REGISTRY = {}
        cls._VIEW_REGISTRY[id_value] = schema
        cls._ID_REGISTRY.setdefault(schema, set()).add(id_value)

    def __getitem__(cls, id_value):
        def construct(*args, **kwargs):
            obj = cls(*args, **kwargs)
            if cls.ID_KEY is not None:
                dict.__setitem__(obj, cls.ID_KEY, id_value)
            return obj
        return construct

    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)

        cls._DECODER_MAP = cls.__dict__.get("_DECODER_MAP", {})
        cls._ENCODER_MAP = cls.__dict__.get("_ENCODER_MAP", {})
        cls._KEYS = cls.__dict__.get("_KEYS", set())
        cls._VIEW_REGISTRY = cls.__dict__.get("_VIEW_REGISTRY", {})
        cls._ID_REGISTRY = cls.__dict__.get("_ID_REGISTRY", {})

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
        cls._VIEW_CHAIN = ChainMap(*(
            klass.__dict__["_VIEW_REGISTRY"]
            for klass in cls.__mro__
            if "_VIEW_REGISTRY" in klass.__dict__
        ))
        cls._ID_CHAIN = ChainMap(*(
            klass.__dict__["_ID_REGISTRY"]
            for klass in cls.__mro__
            if "_ID_REGISTRY" in klass.__dict__
        ))

        cls.DECODER = staticmethod(codec_cast(
            cls._DECODER_CHAIN,
            default=cls.DEFAULT_DECODER,
            key_start=cls.KEY_DECODER,
        ))
        cls.ENCODER = staticmethod(codec_cast(
            cls._ENCODER_CHAIN,
            default=cls.DEFAULT_ENCODER,
            key_end=cls.KEY_ENCODER,
        ))

        return cls

    def get_decoders(cls):
        return {k: v.function for k, v in cls._DECODER_CHAIN.items()}

    def get_encoders(cls):
        return {k: v.function for k, v in cls._ENCODER_CHAIN.items()}

    def get_keys(cls):
        return set(cls._KEY_CHAIN)


class FieldInterface(dict, metaclass=FieldMetaclass):
    ID_KEY: Optional[str] = None

    @property
    def current_id(self):
        return dict.get(self, type(self).ID_KEY) if type(self).ID_KEY else None

    @overload
    def interface(self, key: None = None) -> Optional[BaseInterface]: ...
    @overload
    def interface(self, key: type[V]) -> Optional[V]: ...

    def interface(self, key=None) -> Optional[BaseInterface]:
        view_chain = type(self)._VIEW_CHAIN
        id_chain = type(self)._ID_CHAIN
        current_id = self.current_id

        if key is None:
            view_cls = view_chain.get(current_id)
        elif key in view_chain:
            view_cls = view_chain[key] if current_id == key else None
        elif key in id_chain:
            view_cls = key if current_id in id_chain[key] else None
        else:
            view_cls = None

        return view_cls(self) if view_cls is not None else None

    @overload
    def require_interface(self, key: None = None) -> BaseInterface: ...
    @overload
    def require_interface(self, key: type[V]) -> V: ...

    def require_interface(self, key=None) -> BaseInterface:
        result = self.interface(key)
        if result is None:
            raise TypeError(
                f"{type(self).__name__} has no interface for id {self.current_id!r}"
            )
        return result