
from typing import Any, TypeVar, Generic, overload

T = TypeVar("T")

class ObjField(Generic[T]):
    def __init__(self, key: Any) -> None:
        self.key = key

    @overload
    def __get__(self, instance: None, owner: type[Any]) -> "ObjField[T]": ...
    @overload
    def __get__(self, instance: object, owner: type[Any] | None = None) -> T: ...
    def __get__(self, instance: object | None, owner: type[Any] | None = None) -> T | "ObjField[T]":
        if instance is None:
            return self
        return instance.obj[self.key] # type: ignore[attr-defined]

    def __set__(self, instance: Any, value: T) -> None:
        instance.obj[self.key] = value