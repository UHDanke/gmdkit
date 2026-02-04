# Imports
from typing import Callable, Any
from dataclasses import dataclass, field

# Package Imports
from gmdkit.models.object import Object
from gmdkit.mappings import obj_prop, obj_id
from gmdkit.utils.id_functions import obj_can_be_spawned

Func = Callable | None
BoolFunc = Callable | bool | None

ID_MIN = -2147483648
ID_MAX =  2147483647


@dataclass(slots=True)
class Identifier:
    # required
    obj: Object
    obj_prop_id: int | str
    id_val: int | tuple[int]
    id_type: str
    # optional
    default: int | None = None
    fixed: bool = False
    remappable: bool = False
    reference: bool = False
    iterable: bool = False
    id_min: int = ID_MIN
    id_max: int = ID_MAX
    actions: tuple = ()
    replaceable: bool = True
    replace: Func = None
    remaps: dict = field(default_factory=dict)
    # derived
    is_default: bool = field(init=False, default=False)

    def __post_init__(self):
        if self.id_val == self.default:
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


class IDRule:
    __slots__ = (
        "obj_prop_id", "id_type", "id_min", "id_max",
        "condition", "function", "fallback", "replace",
        "fixed", "default", "remappable",
        "iterable", "reference", "actions",
    )

    def __init__(
            self,
            obj_prop_id: int | str,
            id_type: str,
            condition: Func = None,
            function: Func = None,
            fallback: Func = None,
            replace: Func = None,
            fixed: BoolFunc = None,
            remappable: BoolFunc = None,
            default: Any = None,
            iterable: bool = False,
            reference: bool = False,
            id_min: int = ID_MIN,
            id_max: int = ID_MAX,
            actions: tuple = (),
        ):
        self.obj_prop_id = obj_prop_id
        self.id_type = id_type
        self.id_min = id_min
        self.id_max = id_max
        self.condition = condition
        self.function = function
        self.fallback = fallback
        self.replace = replace
        self.fixed = fixed
        self.default = default
        self.remappable = remappable
        self.iterable = iterable
        self.reference = reference
        self.actions = actions


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


class RuleHandler:
    __slots__ = ("base", "by_id")

    def __init__(self, base: tuple[IDRule], by_id: dict[int | str, tuple[IDRule]]):
        self.base  = base  or ()
        self.by_id = by_id or {}

    def get_ids(self, obj: Object):
        oid = obj.get(obj_prop.ID, obj_id.LEVEL_START)

        rules = self.by_id.get(oid)
        if rules is not None:
            for rule in rules:
                yield from rule.get_ids(obj)

        if oid != obj_id.LEVEL_START and self.base:
            for rule in self.base:
                yield from rule.get_ids(obj)

                
class IdentifierList:
    
    def __init__(self):
        self.ids = list()
        self.ignored = set()
        self.min = ID_MIN
        self.max = ID_MAX
    
    
    def get_ids(
        self,
        default:bool|None = None,
        fixed:bool|None = None,
        remappable:bool|None = None,
        reference:bool|None = None,
        in_range:bool = False,
        remap:bool = False,
        condition:Callable|None=None
    ) -> set[int]:

        result = set()
        for i in self.ids:
            
            if in_range and not self.min <= i.get("val",0) <= self.max:
                continue
            
            if default is not None and i.get("default", False) != default:
                continue
            
            if fixed is not None and i.get("fixed", False) != fixed:
                continue
            
            if remappable is not None and i.get("remappable", False) != remappable:
                continue

            if reference is not None and i.get("reference", False) != reference:
                continue
            
            if condition and callable(condition) and not condition(i):
                continue
            
            if remap and (new_ids:=i.get("remaps",set())):
                for n in new_ids:
                    n = min(max(n, self.min), self.max)
                    result.add(n)
            else:
                n = min(max(i.get("val",0), self.min), self.max)
                result.add(n)
        
        return result
    
    
    def get_limits(self):
        self.min = -2147483648
        self.max = 2147483647
        for i in self.ids:
            self.min = max(i.get("min",self.min), self.min)
            self.max = min(i.get("max",self.max), self.max)
        
        return self.min, self.max
    
    
    def add_remaps(self, remaps:dict):
        
        for k,l in remaps.items():                
            group = self.remaps.setdefault(k,set())
            group.update(set(l))
