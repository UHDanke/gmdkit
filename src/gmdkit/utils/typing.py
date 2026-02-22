# Imports
from typing import Any, Protocol, Callable, Iterable
from os import PathLike

    
PathString = str|PathLike
PlistStruct = dict|list|tuple
NumKey = int|str


class Caster(Protocol):
    def __call__(self, value: Any, **kwargs:Any) -> Any : ...

class DictCaster(Protocol):
    def __call__(self, key:NumKey, value: Any, **kwargs:Any) -> tuple[NumKey, Any]: ...
    
    
class StringDecoder(Protocol):
    def __call__(self, value: str, **kwargs:Any) -> Any : ...

class StringEncoder(Protocol):
    def __call__(self, value: Any, **kwargs:Any) -> str : ...

class KeyValueCondition(Protocol):
    def __call__(self, key: Any, value: Any) -> bool : ...

class StringDictDecoder(Protocol):
    def __call__(self, key: str, value: str, **kwargs:Any) -> tuple[NumKey, Any]: ...
    
class StringDictEncoder(Protocol):
    def __call__(self, key:NumKey, value:Any, **kwargs:Any) -> tuple[str, str]: ...


class PlistWrapper(Protocol):
    def __call__(self, data:Any, func:Callable, **kwargs) -> Any: ...
    
class DictWrapper(Protocol):
    def __call__(self, data:dict, func:DictCaster, **kwargs) -> dict: ...
    
class ArrayWrapper(Protocol):
    def __call__(self, data:Iterable, func:Caster, **kwargs) -> list: ...