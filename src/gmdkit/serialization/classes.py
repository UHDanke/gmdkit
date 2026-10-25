# Imports
from typing import Callable, Any, Optional, TypeVar, overload, Type, Union, ClassVar, Self
from collections import ChainMap
from operator import attrgetter

# Package Imports
from gmdkit.utils.typing import MISSING
from gmdkit.utils.types import DictClass
from gmdkit.serialization.functions import (
    read_plist, write_plist, codec_cast
    )

 
class LazyString:
    
    __slots__ = ("string", "data")
 
    PARSER: ClassVar[type]
 
    def __init__(self, string: str = "", data: Optional[Any] = None):
        self.string = string
        self.data = data
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        reserved = {name for klass in LazyString.__mro__ for name in vars(klass)
                    if not name.startswith("__")} - {"PARSER"}
        clashes = sorted(reserved & vars(cls).keys())
        if clashes:
            raise TypeError(
                f"{cls.__name__} redefines reserved LazyString attribute(s) {clashes}; "
                f"use another name, e.g. `my_{clashes[0]} = LazyAttr({clashes[0]!r})`"
            )
 
    @property
    def loaded(self) -> bool:
        return self.data is not None
 
    def load(self) -> Any:
        """Parse the string into data and return it."""
        self.data = self.PARSER.from_string(self.string)
        return self.data
 
    def save(self) -> str:
        if self.data is not None:
            self.string = self.data.to_string()
        return self.string
 
    @classmethod
    def load_string(cls, string: str) -> Self:
        return cls(string)
 
    def save_string(self) -> str:
        return self.save()
    
    def __repr__(self) -> str:
        string = self.string if len(self.string) <= 40 else self.string[:37] + "..."
        state = f"<{type(self.data).__name__}>" if self.loaded else "<unloaded>"
        return f"{type(self).__name__}({string!r}, {state})"
 
class LazyAttr:
    
    def __init__(self, name: str = None):
        self.name = name

    def __set_name__(self, owner, name):
        self.name = self.name or name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if instance.data is None:
            instance.load()
        return getattr(instance.data, self.name)

    def __set__(self, instance, value):
        if instance.data is None:
            instance.load()
        setattr(instance.data, self.name, value)

class AliasAttr:
    
    def __init__(self, path: str):
        self.path = path
        *parent, self.attr = path.split(".")
        self.parent = attrgetter(".".join(parent)) if parent else (lambda obj: obj)

    def __get__(self, instance: Any, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(self.parent(instance), self.attr)

    def __set__(self, instance: Any, value: Any) -> None:
        setattr(self.parent(instance), self.attr, value)
        
class BaseInterface:
    CONTAINER = "obj"

    def __init__(self, obj: "FieldInterface"):
        self.obj = obj

    def __getattr__(self, name: str) -> Any:
        d = object.__getattribute__(self, "__dict__")

        if "obj" not in d:
            raise AttributeError(name)

        return getattr(d["obj"], name)
    
    def has_field(self, name: str) -> bool:
        field = getattr(type(self), name, None)
        if not isinstance(field, AliasField):
            raise AttributeError(f"{type(self).__name__} has no field {name!r}")
        return field.canonical in self.obj

    def __getitem__(self, key):
        return self.obj[key]

    def __setitem__(self, key, value):
        self.obj[key] = value

    def __delitem__(self, key):
        del self.obj[key]

    def __contains__(self, key):
        return key in self.obj

    def __len__(self):
        return len(self.obj)

    def __iter__(self):
        return iter(self.obj)

    def __repr__(self):
        return f"{type(self).__name__}({self.obj!r})"

V = TypeVar("V", bound=BaseInterface)
T = TypeVar("T")

class Default:
    __slots__ = ("value", "factory","pass_kwargs")

    def __init__(self, value=MISSING, factory=None, pass_kwargs:bool=False):
        if factory is not None and value is not MISSING:
            raise ValueError("pass either default or default_factory, not both")
        self.value = value
        self.factory = factory
        self.pass_kwargs = pass_kwargs

    @property
    def stored(self):
        return self.factory is not None

    def __call__(self, **kwargs):
        if self.factory is not None:
            return self.factory(**kwargs) if self.pass_kwargs else self.factory()
        else:
            return self.value

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


class AliasField:
    def __init__(self, canonical: str = None, read_only: bool = False):
        self.canonical = canonical
        self.read_only = read_only

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
        if self.read_only:
            raise AttributeError(f"{type(instance).__name__}.{self.name} is read-only")
        self._target(instance)[self.canonical] = value

    def __delete__(self, instance):
        if self.read_only:
            raise AttributeError(f"{type(instance).__name__}.{self.name} is read-only")
        del self._target(instance)[self.canonical]

class DictField(AliasField):
    def __init__(self, key=None, default=MISSING, default_factory=None, default_callable=None,
                 encoder=None, decoder=None, is_node=False, pass_kwargs=False):
        super().__init__(key)
        self.default = default
        self.default_factory = default_factory
        self.default_callable = default_callable
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
            default=self.default,
            default_factory=self.default_factory,
            default_callable=self.default_callable
        )


class FieldMetaclass(type):
    KEY_DECODER: Optional[Callable] = None
    KEY_ENCODER: Optional[Callable] = None

    DEFAULT_DECODER: Callable = staticmethod(read_plist)
    DEFAULT_ENCODER: Callable = staticmethod(write_plist)
    DECODER: Callable
    ENCODER: Callable
    HAS_NODES: bool = False

    _ENCODER_MAP: dict
    _DECODER_MAP: dict
    _DEFAULT_MAP: dict
    _KEYS: set
    _ENCODER_CHAIN: ChainMap
    _DECODER_CHAIN: ChainMap
    _DEFAULT_CHAIN: ChainMap
    _KEY_CHAIN: ChainMap

    def add_field(cls, key, *, encoder=None, decoder=None, is_node=False,
                  pass_kwargs=False, default=MISSING, default_factory=None, default_callable=None):
        if "_KEYS" not in cls.__dict__:
            cls._KEYS = set()
        if key in cls._KEYS:
            raise RuntimeError(f"a field with key '{key}' already exists")
        cls._KEYS.add(key)
        if encoder is not None:
            if "_ENCODER_MAP" not in cls.__dict__:
                cls._ENCODER_MAP = {}
            codec_cls = EncoderCodec if (cls.HAS_NODES and not is_node) else Codec
            cls._ENCODER_MAP[key] = codec_cls(encoder, allow_kwargs=pass_kwargs)
        if decoder is not None:
            if "_DECODER_MAP" not in cls.__dict__:
                cls._DECODER_MAP = {}
            codec_cls = DecoderCodec if (cls.HAS_NODES and not is_node) else Codec
            cls._DECODER_MAP[key] = codec_cls(decoder, allow_kwargs=pass_kwargs)
        if default_callable is not None or default_factory is not None or default is not MISSING:
            if "_DEFAULT_MAP" not in cls.__dict__:
                cls._DEFAULT_MAP = {}
            cls._DEFAULT_MAP[key] = Default(
                default, 
                default_callable or default_factory, 
                default_callable is not None
                )

    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        cls.__missing__ = mcls._missing
        cls._DECODER_MAP = cls.__dict__.get("_DECODER_MAP", {})
        cls._ENCODER_MAP = cls.__dict__.get("_ENCODER_MAP", {})
        cls._DEFAULT_MAP = cls.__dict__.get("_DEFAULT_MAP", {})
        cls._KEYS = cls.__dict__.get("_KEYS", set())

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
        cls._DEFAULT_CHAIN = ChainMap(*(
            klass.__dict__["_DEFAULT_MAP"]
            for klass in cls.__mro__
            if "_DEFAULT_MAP" in klass.__dict__
        ))
        cls._KEY_CHAIN = ChainMap(*(
            klass.__dict__["_KEYS"]
            for klass in cls.__mro__
            if "_KEYS" in klass.__dict__
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
    
    def _missing(self, key):
        cls = type(self)
        default = cls._DEFAULT_CHAIN.get(key)
        
        if default is None:
            raise KeyError(f"{key!r} is missing and has no default or default_factory")
            
        value = default(owner=self)
        if default.stored:
            dict.__setitem__(self, key, value)
        return value

    def get_decoders(cls):
        return {k: v.function for k, v in cls._DECODER_CHAIN.items()}

    def get_encoders(cls):
        return {k: v.function for k, v in cls._ENCODER_CHAIN.items()}

    def get_keys(cls):
        return set().union(*(
            klass.__dict__["_KEYS"]
            for klass in cls.__mro__
            if "_KEYS" in klass.__dict__
        ))

    def get_defaults(cls):
        return {key: default() for key, default in cls._DEFAULT_CHAIN.items()}


class InterfaceMetaclass(FieldMetaclass):
    DEFAULT_SCHEMA: Type[BaseInterface] = BaseInterface
    ID_KEY: Optional[str] = None

    _VIEW_REGISTRY: dict
    _ID_REGISTRY: dict
    _VIEW_CHAIN: ChainMap
    _ID_CHAIN: ChainMap

    def register_id(cls, id_value, schema: Type[BaseInterface]):
        if not (isinstance(schema, type) and issubclass(schema, BaseInterface)):
            raise TypeError(f"{schema!r} must be a subclass of BaseInterface")
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

        cls._VIEW_REGISTRY = cls.__dict__.get("_VIEW_REGISTRY", {})
        cls._ID_REGISTRY = cls.__dict__.get("_ID_REGISTRY", {})

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

        return cls

    def get_schema(cls, id_value=None):
        return cls._VIEW_CHAIN.get(id_value, cls.DEFAULT_SCHEMA)


class FieldInterface(DictClass, metaclass=InterfaceMetaclass):

    @property
    def current_id(self):
        return dict.get(self, type(self).ID_KEY) if type(self).ID_KEY else None
    
    @property
    def interface(self) -> BaseInterface:
        schema = type(self).get_schema(self.current_id)
        return schema(self)
    
    @overload
    def require_interface(self, cls: Type[V]) -> V: ...
    @overload
    def require_interface(self, cls: Type[V], fallback: T) -> Union[V,T]: ...
    def require_interface(self, cls, fallback=MISSING):
        schema = type(self).get_schema(self.current_id)
        if issubclass(schema, cls):
            return schema(self)
        if fallback is not MISSING:
            return fallback
        raise TypeError(...)
    
    @overload
    def require_interface_by_id(self, id: int | str) -> BaseInterface: ...
    @overload
    def require_interface_by_id(self, id: int | str, fallback: T) -> BaseInterface | T: ...
    def require_interface_by_id(self, id, fallback=MISSING):
        if id == self.current_id:
            return self.interface
        if fallback is not MISSING:
            return fallback
        raise TypeError(...)