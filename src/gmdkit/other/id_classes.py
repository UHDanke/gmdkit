# Imports
from typing import Callable, Any, Optional, Sequence
from dataclasses import dataclass, field
from enum import IntEnum

# Package Imports
from gmdkit.models.object import Object
from gmdkit.mappings import obj_prop, obj_id
from gmdkit.other.id_functions import obj_can_be_spawned


ID_MIN = -2147483648
ID_MAX =  2147483647


class IDType(IntEnum):
    GROUP_ID = 0  
    ITEM_ID = 1
    TIME_ID = 2
    COLLISION_ID = 3
    COLOR_ID = 4
    CONTROL_ID = 5
    LINK_ID = 6
    TRIGGER_CHANNEL = 7
    ENTER_CHANNEL = 8
    MATERIAL_ID = 9
    EFFECT_ID = 10
    GRADIENT_ID = 11
    FORCE_ID = 12
    KEYFRAME_ID = 13
    SFX_ID = 14
    SONG_ID = 15
    UNIQUE_SFX_ID = 16
    SFX_GROUP = 17
    SONG_CHANNEL = 18
    REMAP_BASE = 19
    REMAP_TARGET = 20


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


@dataclass(slots=True)
class Identifier:
    # required
    obj: Object
    obj_prop_id: int | str
    id_val: int | tuple[int]
    id_type: IDType
    # optional
    default: Optional[int] = None
    fixed: bool = False
    remappable: bool = False
    reference: bool = False
    iterable: bool = False
    id_min: int = ID_MIN
    id_max: int = ID_MAX
    actions: tuple[IDActions] = ()
    replaceable: bool = True
    replace: Optional[Callable] = None
    remaps: dict = field(default_factory=dict)
    # derived
    is_default: bool = field(init=False, default=False)

    def __post_init__(self):
        
        if type(self.id_val) is tuple:
            self.iterable = True
            
        elif self.id_val == self.default:
            self.is_default = True
            self.fixed = True


    def remap_obj(self, kv_map: dict, override: bool = False) -> None:
        if not override and (self.fixed or self.default) or not kv_map:
            return

        if callable(self.replace):
            val = self.obj.get(self.obj_prop_id)
            if val is not None:
                self.replace(val, kv_map)

        elif (new := kv_map.get(self.id_val)) is not None:
            self.obj[self.obj_prop_id] = new


@dataclass(slots=True)
class IDRule:
    obj_prop_id: int | str
    id_type: str
    condition: Optional[Callable] = None
    function: Optional[Callable] = None
    fallback: Optional[Callable] = None
    replace: Optional[Callable] = None
    fixed: Optional[Callable|bool] = None
    remappable: Optional[Callable|bool] = None
    default: Any = None
    iterable: bool = False
    reference: bool = False
    id_min: int = ID_MIN
    id_max: int = ID_MAX
    actions: Optional[tuple] = None

    def get_ids(self, obj: Object):
        val = obj.get(self.obj_prop_id)
        
        default = self.default(obj) if callable(self.default) else self.default

        if val is None:
            if callable(self.fallback):
                val = self.fallback(obj)
            if val is None:
                if default is None:
                    return
                val = default
    
        if callable(self.condition) and not self.condition(obj):
            return
    
        if callable(self.function):
            val = self.function(val)
    
        if self.iterable:
            val = tuple(val)
            if not val:
                return
        elif val is None:
            return
        
        fixed = self.fixed(obj) if callable(self.fixed) else self.fixed
        remappable = self.remappable(obj) if callable(self.remappable) else self.remappable
    
        return Identifier(
            obj=obj,
            obj_prop_id =self.obj_prop_id,
            id_val = val,
            id_type = self.id_type,
            default = default,
            fixed = bool(fixed),
            remappable = bool(remappable) and obj_can_be_spawned(obj),
            reference = self.reference,
            iterable = self.iterable,
            id_min = self.id_min,
            id_max = self.id_max,
            actions = self.actions,
            replace = self.replace,
        )


@dataclass(slots=True)
class RuleHandler:
    
    base: tuple[IDRule] = field(default_factory=tuple)
    by_id: dict[int|str, tuple[IDRule]] = field(default_factory=dict)

    def get_ids(self, obj: Object):
        
        oid = obj.get(obj_prop.ID, obj_id.LEVEL_START)
        rules = self.by_id.get(oid)
        
        if rules is not None:
            for rule in rules:
                yield from rule.get_ids(obj)

        if oid != obj_id.LEVEL_START and self.base:
            for rule in self.base:
                yield from rule.get_ids(obj)


@dataclass(slots=True)           
class IdentifierList:
    
    ids: list[Identifier] = field(default_factory=list)
    ignored: set[int] = field(default_factory=set)
    vmin: int = ID_MIN
    vmax: int = ID_MAX
    
    def get_ids(
            self,
            default:Optional[bool] = None,
            fixed:Optional[bool] = None,
            remappable:Optional[bool] = None,
            reference:Optional[bool] = None,
            in_range:bool = False,
            remap:bool = False,
            condition:Optional[Callable]=None,
            has_tags:Optional[Sequence[str]]=None,
            ) -> set[int]:

        result = set()
        
        has_cond = callable(condition)
        
        for i in self.ids:
            
            
            if in_range and not self.min <= i.id_val <= self.max:
                continue
            
            if default is not None and i.default != default:
                continue
            
            if fixed is not None and i.fixed != fixed:
                continue
            
            if remappable is not None and i.remappable != remappable:
                continue

            if reference is not None and i.reference != reference:
                continue
            
            if has_cond and not condition(i):
                continue
            
            if has_tags:
                continue
            
            if remap and (new_ids:=i.remaps):
                for n in new_ids:
                    n = min(max(n, self.vmin), self.vmax)
                    result.add(n)
            else:
                n = min(max(i.id_val, self.vmin), self.vmax)
                result.add(n)
        
        return result
    
    
    def get_limits(self):
        
        self.vmin = ID_MIN
        self.vmax = ID_MAX
        
        for i in self.ids:
            self.min = max(i.vmin, self.min)
            self.max = min(i.vmax, self.max)
        
        return self.min, self.max