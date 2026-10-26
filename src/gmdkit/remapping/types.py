# Imports
import re
from enum import IntEnum, IntFlag
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
    ANIMATION_ID = 1015
    PLAYER_ID = 1016
    # gmdkit types
    LABEL = 2002
    GENERIC = 2001


class IDActions(IntFlag):
    NONE = 0
    ACTIVE = 1 << 0
    SPAWN = 1 << 1
    TOGGLE = 1 << 2
    FOLLOW_POSITION = 1 << 3
    COLOR = 1 << 4
    FOLLOW_COLOR = 1 << 5
    ALPHA = 1 << 6
    FOLLOW_ALPHA = 1 << 7
    MOVE = 1 << 8
    FOLLOW_MOVE = 1 << 9
    ROTATE = 1 << 10
    FOLLOW_ROTATE = 1 << 11
    SCALE = 1 << 12
    FOLLOW_SCALE = 1 << 13
    ANIMATE = 1 << 14
    KEYFRAME = 1 << 15
    PARTICLES = 1 << 16
    UI = 1 << 17
    RESET = 1 << 18
    STOP = 1 << 19
    PAUSE = 1 << 20
    RESUME = 1 << 21
    EDIT_EFFECT = 1 << 22
    STOP_EFFECT = 1 << 23
    SET_ITEM = 1 << 24
    GET_ITEM = 1 << 25
    TRACK_ITEM = 1 << 26
    PERSIST_ITEM = 1 << 27
    TRACK_COLLISION = 1 << 28
    CHECK_COLLISION = 1 << 29
    LINKED_OBJECTS = 1 << 30


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


SPAWNABLE_TRIGGERS = frozenset((
    29, 30, 32, 33, 105, 744, 899, 900, 901, 915, 1006, 1007, 1049, 1268, 1346, 1347, 1520, 1585,
    1595, 1611, 1612, 1613, 1616, 1811, 1812, 1814, 1815, 1817, 1818, 1819, 1912, 1913, 1914, 1916,
    1917, 1931, 1932, 1934, 1935, 2015, 2062, 2063, 2066, 2067, 2068, 2899, 2900, 2901, 2903, 2904,
    2905, 2907, 2909, 2910, 2911, 2912, 2913, 2914, 2915, 2916, 2917, 2919, 2920, 2921, 2922, 2923,
    2924, 2925, 2999, 3006, 3007, 3008, 3009, 3010, 3011, 3012, 3013, 3014, 3015, 3016, 3017, 3018,
    3019, 3020, 3021, 3022, 3023, 3024, 3029, 3030, 3031, 3033, 3600, 3602, 3603, 3604, 3605, 3606,
    3607, 3608, 3609, 3612, 3613, 3614, 3615, 3617, 3618, 3619, 3620, 3640, 3641, 3655, 3660, 3661,
    3662, 3663,
    ))