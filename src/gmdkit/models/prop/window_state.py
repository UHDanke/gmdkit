# Imports
from typing import Any, Optional

# Package Imports
from gmdkit.utils import enums


class WindowStateField:
    def __init__(self, key: str, type: type, default: Any):
        self.key = key
        self.type = type
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        index = instance.find_index()
        if index is None:
            return self.default
        return instance.obj.get(f"ws_{index}_{self.key}", self.default)

    def __set__(self, instance, value):
        index = instance.find_index()
        if index is None:
            raise KeyError(f"{instance.window_id.name} has no saved state, call create() first")
        instance.obj[f"ws_{index}_{self.key}"] = self.type(value)


class WindowState:
    COUNT_KEY = "winStateCount"

    center_x: float = WindowStateField("cx", float, 0.0)
    center_y: float = WindowStateField("cy", float, 0.0)
    width: float = WindowStateField("w", float, 0.0)
    height: float = WindowStateField("h", float, 0.0)
    scale: float = WindowStateField("s", float, 1.0)
    scroll_offset: float = WindowStateField("so", float, 0.0)
    version: int = WindowStateField("v", int, 1)

    def __init__(self, obj, window_id: enums.EditorWindow | int):
        self.obj = obj
        self.window_id = enums.EditorWindow(window_id)

    @classmethod
    def fields(cls) -> dict[str, WindowStateField]:
        return {
            name: field
            for klass in reversed(cls.__mro__)
            for name, field in vars(klass).items()
            if isinstance(field, WindowStateField)
        }

    def find_index(self) -> Optional[int]:
        obj = self.obj
        window_id = int(self.window_id)
        for index in reversed(range(obj.get(type(self).COUNT_KEY, 0))):
            if obj.get(f"ws_{index}_k") == window_id:
                return index
        return None

    def exists(self) -> bool:
        return self.find_index() is not None

    def create(self, center_x: float, center_y: float, **values: Any) -> int:
        fields = type(self).fields()
        unknown = set(values) - set(fields)
        if unknown:
            raise TypeError(f"unknown window state fields: {', '.join(sorted(unknown))}")
        values["center_x"] = center_x
        values["center_y"] = center_y

        index = self.find_index()
        obj = self.obj
        if index is None:
            index = obj.get(type(self).COUNT_KEY, 0)
            obj[type(self).COUNT_KEY] = index + 1
        obj[f"ws_{index}_k"] = int(self.window_id)
        for name, field in fields.items():
            obj[f"ws_{index}_{field.key}"] = field.type(values.get(name, field.default))
        return index

    def remove(self):
        index = self.find_index()
        if index is None:
            return
        obj = self.obj
        count = obj.get(type(self).COUNT_KEY, 0)
        for key in [k for k in obj if isinstance(k, str) and k.startswith(f"ws_{index}_")]:
            del obj[key]
        for source in range(index + 1, count):
            old = f"ws_{source}_"
            new = f"ws_{source - 1}_"
            for key in [k for k in obj if isinstance(k, str) and k.startswith(old)]:
                obj[new + key[len(old):]] = obj.pop(key)
        obj[type(self).COUNT_KEY] = count - 1

    def to_dict(self) -> dict:
        return {name: getattr(self, name) for name in type(self).fields()}

    def __repr__(self):
        return f"{type(self).__name__}({self.window_id.name}, {self.find_index()}, {self.to_dict()!r})"