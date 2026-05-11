# Imports
from typing import Callable, Any, Optional, Sequence, Iterable, Self
from dataclasses import dataclass, field
from enum import IntEnum

# Package Imports
from gmdkit import Level, Object, ObjectList
from gmdkit.mappings import obj_prop, obj_id
from gmdkit.other.id_functions import obj_can_be_spawned


ID_MIN = -2147483648
ID_MAX =  2147483647


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
    
IDGroup = Sequence[IDType]

AnyID = IDType.ANY

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


class AutoID:
    __slots__ = ()
    
    def __setattr__(self, name, value):
        raise TypeError("immutable")

    def __repr__(self):
        return f"<AutoID at {hex(id(self))}>"

    def __copy__(self):
        return type(self)()

    def __deepcopy__(self, memo):
        oid = id(self)
        if oid in memo:
            return memo[oid]

        obj = type(self)()
        memo[oid] = obj
        return obj


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
    # derived
    is_default: bool = field(init=False, default=False)

    def __post_init__(self):
        
        if type(self.id_val) is tuple and not self.iterable:
            self.iterable = True
            
        if not self.iterable and self.id_val == self.default:
            self.is_default = True
            #self.fixed = True


    def remap_obj(self, kv_map:dict, override:bool=False):
        if not override and self.fixed or not kv_map:
            return
        obj = self.obj
        pid = self.obj_prop_id
        
        if self.replace is not None and callable(self.replace):
            val = obj.get(pid)
            
            if val is not None:
                obj[pid] = self.replace(val, kv_map)
                
        elif (new := kv_map.get(self.id_val)) is not None:
            obj[pid] = new


@dataclass(slots=True)           
class IdentifierList:
    
    values: tuple[Identifier] = field(default_factory=tuple)
    ignored: set[int] = field(default_factory=set)
    vmin: int = ID_MIN
    vmax: int = ID_MAX        
    
    def __post_init__(self):
        if type(self.values) is not tuple:
            self.values = tuple(self.values)
        self.get_limits()
        
    def get_limits(self) -> (int,int):
        self.vmin = max((i.id_min for i in self.values), default=ID_MIN)
        self.vmax = min((i.id_max for i in self.values), default=ID_MAX)
        return self.vmin, self.vmax

    def filter_values(
            self,
            default:Optional[bool] = None,
            fixed:Optional[bool] = None,
            remappable:Optional[bool] = None,
            reference:Optional[bool] = None,
            condition:Optional[Callable]=None,
            has_tags:Optional[Sequence[IDActions]]=None,
            has_types:Optional[Sequence[IDType]]=None
            ) -> set[int]:

        result = []
        has_cond = callable(condition)
        
        for i in self.values:
            
            if has_types and i.id_type not in has_types:
                continue
            
            if default is not None and i.is_default != default:
                continue
            
            if fixed is not None and i.fixed != fixed:
                continue
            
            if remappable is not None and i.remappable != remappable:
                continue

            if reference is not None and i.reference != reference:
                continue
            
            if has_cond and not condition(i):
                continue
            
            if has_tags and i.actions not in i.has_tags:
                continue
            
            result.append(i)
        
        return self.__class__(values=result)
    
    def get_ids(
            self,
            in_range:bool = False,
            min_value:Optional[int] = None,
            max_value:Optional[int] = None
            ) -> set|dict[set]:
        
        ids = self.values        
        low = min_value if min_value is not None else self.vmin
        high = max_value if max_value is not None else self.vmax
        
        result = set()
        
        for i in ids:
            vals = i.id_val if i.iterable else (i.id_val,)
        
            for v in vals:
                
                if in_range and (type(v) is AutoID or not (low <= v <= high)):
                    continue
                
                result.add(v)
        
        return result

    def remap_objects(self, kv_map:dict, override:bool=False):
        
        if not kv_map:
            return
        
        for v in self.values:
            v.remap_obj(kv_map=kv_map,override=override)
    
    def get_objects(self, condition: Optional[Callable] = None) -> ObjectList:
        
        seen = set()  
        new = ObjectList()
        
        for i in self.values:
            obj = i.obj
            
            if obj is None:
                continue
            
            obj_str = obj.to_string(sort_keys=True)
            
            if obj_str in seen: 
                continue
            
            if condition is not None and callable(condition) and not condition(i):
                continue
            
            new.append(obj)
            seen.add(obj_str)
        
        return new
    
    @staticmethod    
    def group_by_type(
            identifiers:Sequence[Identifier],
            type_groups:Sequence[Sequence[IDType]]
            ):
        
        seen = set()
        id_dict = {}        
        
        for i in identifiers:
            id_dict.setdefault(i.id_type,[]).append(i)
        
        if type_groups is None:
            return {k: IdentifierList(values=v) for k,v in id_dict.items()}
        
        result = {}
        
        for k in type_groups:
            seen.update(k)
            result[k] = tuple(
                v
                for t in k if t in id_dict
                for v in id_dict[t]
            )

        for k in set(id_dict.keys()) - seen:
            result[k] = id_dict[k]
            
        return {k: IdentifierList(values=v) for k,v in result.items()}


@dataclass(slots=True,frozen=True)
class IDRule:
    obj_prop_id: int | str
    id_type: IDType
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
    
    def is_matched(
            self,
            id_types:Optional[Sequence[IDType]]=None,
            reference:Optional[bool]=None,
            actions: Optional[tuple]=None
            ):
        if id_types and self.id_type not in id_types:
            return False
        if reference is not None and self.reference != reference:
            return False
        if actions and self.id_type not in id_types:
            return False
        return True
        
    def get_id(self, obj: Object):
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
            fixed = self.fixed
        elif val is None:
            return
        
        else:            
            fixed = self.fixed(val) if callable(self.fixed) else self.fixed
        
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
    
    def compile_rules(self, **kwargs):
        
        base = tuple(i for i in self.base if i.is_matched(**kwargs))
        by_id = {}
        
        for k, v in self.by_id.items():
            r = tuple(i for i in v if i.is_matched(**kwargs))
            if r:
                by_id[k] = r
            
        return self.__class__(base=base,by_id=by_id)
    
    def combine_rules(self, *rules):
        
        base = set()
        by_id = {}
        rule_list = [self, *rules]
        
        for r in rule_list:
            base.update(r.base)
            
            for k,v in r.by_id.items():
                by_id.setdefault(k,set()).update(v)
        
        return self.__class__(base=tuple(base),by_id={k:tuple(v) for k,v in by_id.items()})
    
    def fetch_ids(
            self,
            obj:Object
            ):
        
        result = []
        oid = obj.get(obj_prop.ID, 0)
        rules = self.by_id.get(oid)
        
        if rules is not None:
            for rule in rules:
                if (i:= rule.get_id(obj)) is not None:
                    result.append(i)
    
        if oid != obj_id.LEVEL_START and self.base:
            for rule in self.base:
                if (i:= rule.get_id(obj)) is not None:
                    result.append(i)
        
        return tuple(result)
        
    def compile_ids(
            self, 
            source: ObjectList|Level,
            by_type:bool=False,
            type_groups:Optional[Sequence[set]]=None
            ) -> IdentifierList|dict[Sequence[IDType]|IDType,IdentifierList]:
        
        result = []
        cls = type(source)
        
        if issubclass(cls, Level):
            result.extend(self.fetch_ids(source.start))
            for obj in source.objects:
                result.extend(self.fetch_ids(obj))
                
        elif issubclass(cls, ObjectList):            
            for obj in source:
                result.extend(self.fetch_ids(obj))
        
        else:
            for obj in source:
                result.extend(self.fetch_ids(obj))
        
        if by_type:
            return IdentifierList.group_by_type(result, type_groups)
        return IdentifierList(values=result)