# Imports
import re
from enum import IntEnum
from dataclasses import dataclass
from typing import ClassVar, get_type_hints, Optional, Self

# Package Imports
from gmdkit.utils.functions import typed_cache


class AutoID:
    __slots__ = ("index",)
    counter = 1

    def __new__(cls):
        obj = object.__new__(cls)
        object.__setattr__(obj, "index", cls.counter)
        cls.counter += 1
        return obj
    
    def __getstate__(self):
        return (self.index,)

    def __setstate__(self, state):
        object.__setattr__(self, "index", state[0])

    def __setattr__(self, name, value):
        raise TypeError("AutoID is immutable")

    def __repr__(self):
        return f"<AutoID #{self.index}>"

    def __copy__(self):
        return type(self)()

    def __deepcopy__(self, memo):
        oid = id(self)
        if oid in memo:
            return memo[oid]
        obj = type(self)()
        memo[oid] = obj
        return obj

    def __lt__(self, other):
        return self.index < other.index

@dataclass
class LabelID:
    template: str
    value: int = 0
    text: str = ""

    _TYPE_TO_PATTERN: ClassVar[dict] = {
        int: r"\d+",
        float: r"\d+\.\d+",
        str: r"\w+",
    }

    @classmethod
    @typed_cache()
    def _hints(cls) -> dict:
        return {k: v for k, v in get_type_hints(cls).items()
                if not k.startswith("_") and k != "template"}

    @classmethod
    @typed_cache()
    def _build_pattern(cls, template: str) -> str:
        pattern = re.escape(template)
        for field_name, field_type in cls._hints().items():
            field_pattern = cls._TYPE_TO_PATTERN.get(field_type, r"\w+")
            pattern = pattern.replace(
                re.escape(f"{{{field_name}}}"),
                f"(?P<{field_name}>{field_pattern})"
            )
        return pattern

    def __str__(self) -> str:
        return self.template.format(**{f: getattr(self, f) for f in self._hints()})

    @classmethod
    def from_string(cls, formatted: str, template: str) -> Optional[Self]:
        match = re.fullmatch(cls._build_pattern(template), formatted)
        if not match:
            return None
        kwargs = {k: cls._hints()[k](v) for k, v in match.groupdict().items()}
        return cls(template=template, **kwargs)


class IDType(IntEnum):
    ANY = 0
    # in-game types
    GROUP_ID = 1
    ITEM_ID = 2
    COLLISION_ID = 3
    TIMER_ID = 4
    EFFECT_ID = 5
    CONTROL_ID = 6
    GRADIENT_ID = 7
    ENTER_CHANNEL = 8
    # unmapped game types
    COLOR_ID = 1001
    LINK_ID = 1002
    TRIGGER_CHANNEL = 1003
    MATERIAL_ID = 1004
    FORCE_ID = 1005
    KEYFRAME_ID = 1006
    SFX_ID = 1007
    CUSTOM_SFX_ID = 1008
    SONG_ID = 1009
    UNIQUE_SFX_ID = 1010
    SFX_GROUP = 1011
    SONG_CHANNEL = 1012
    REMAP_BASE = 1013
    REMAP_TARGET = 1014
    # gmdkit types
    LABEL = 2002
    GENERIC = 2001


class IDActions(IntEnum):
    SINGLE = 0
    ACTIVE = 1
    SPAWN = 2
    TOGGLE = 3
    FOLLOW_POSITION = 4 
    COLOR = 5
    FOLLOW_COLOR = 6
    ALPHA = 7
    FOLLOW_ALPHA = 8
    MOVE = 9
    FOLLOW_MOVE = 10
    ROTATE = 11
    FOLLOW_ROTATE = 12
    SCALE = 13
    FOLLOW_SCALE = 14
    ANIMATE = 15
    KEYFRAME = 16
    PARTICLES = 17
    UI = 18
    RESET = 19
    STOP = 20
    PAUSE = 21
    RESUME = 22
    EDIT_EFFECT = 23
    STOP_EFFECT = 24
    SET_ITEM = 25
    GET_ITEM = 26
    TRACK_ITEM = 27
    PERSIST_ITEM = 28
    TRACK_COLLISION = 29
    CHECK_COLLISION = 30
    LINKED_OBJECTS = 31
    

class IDGroup:
    def __init__(self, name: str, *members: IDType):
        self.name = name
        self.members = members
    
    def __repr__(self):
        return f"<IDGroup: '{self.name}'>"
    
    def __iter__(self):
        return iter(self.members)

    def __contains__(self, item):
        return item in self.members