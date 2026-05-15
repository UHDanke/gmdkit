# Imports
from enum import IntEnum
from dataclasses import dataclass


class AutoID:
    __slots__ = ("index",)
    counter = 1

    def __new__(cls):
        obj = object.__new__(cls)
        object.__setattr__(obj, "index", cls.counter)
        cls.counter += 1
        return obj

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


@dataclass(frozen=True, slots=True)
class LabelID:
    value: int
    template: str = ""

    def __str__(self) -> str:
        return self.template.format(self.value)
        

class IDType(IntEnum):
    LABEL = -2
    GENERIC = -1
    ANY = 0
    GROUP_ID = 1  
    ITEM_ID = 2
    TIME_ID = 3
    COLLISION_ID = 4
    COLOR_ID = 5
    CONTROL_ID = 6
    LINK_ID = 7
    TRIGGER_CHANNEL = 8
    ENTER_CHANNEL = 9
    MATERIAL_ID = 10
    EFFECT_ID = 11
    GRADIENT_ID = 12
    FORCE_ID = 13
    KEYFRAME_ID = 14
    SFX_ID = 15
    SONG_ID = 16
    UNIQUE_SFX_ID = 17
    SFX_GROUP = 18
    SONG_CHANNEL = 19
    REMAP_BASE = 20
    REMAP_TARGET = 21


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