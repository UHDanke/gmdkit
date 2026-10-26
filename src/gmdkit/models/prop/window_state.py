# Imports
from typing import Any, Optional

# Package Imports
from gmdkit.utils import enums


class WindowStateField:
    def __init__(self, key: str, default: Any):
        self.key = key
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
            index = instance.create()
        instance.obj[f"ws_{index}_{self.key}"] = value


class WindowState:
    COUNT_KEY = "winStateCount"

    center_x: float = WindowStateField("cx", 0.0)
    center_y: float = WindowStateField("cy", 0.0)
    width: float = WindowStateField("w", 0.0)
    height: float = WindowStateField("h", 0.0)
    scale: float = WindowStateField("s", 1.0)
    scroll_offset: float = WindowStateField("so", 0.0)
    version: int = WindowStateField("v", 1)

    def __init__(self, obj, window_id: enums.EditorWindow | int):
        self.obj = obj
        self.window_id = enums.EditorWindow(window_id)

    def find_index(self) -> Optional[int]:
        obj = self.obj
        window_id = int(self.window_id)
        for index in range(obj.get(type(self).COUNT_KEY, 0)):
            if obj.get(f"ws_{index}_k") == window_id:
                return index
        return None

    def exists(self) -> bool:
        return self.find_index() is not None

    def create(self) -> int:
        obj = self.obj
        index = obj.get(type(self).COUNT_KEY, 0)
        obj[f"ws_{index}_k"] = int(self.window_id)
        for name, field in vars(type(self)).items():
            if isinstance(field, WindowStateField):
                obj[f"ws_{index}_{field.key}"] = field.default
        obj[type(self).COUNT_KEY] = index + 1
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
        return {
            name: getattr(self, name)
            for name, field in vars(type(self)).items()
            if isinstance(field, WindowStateField)
        }

    def __repr__(self):
        return f"{type(self).__name__}({self.window_id.name}, {self.find_index()}, {self.to_dict()!r})"