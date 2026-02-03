# Imports
from typing import Callable, Any

# Package Imports
from gmdkit.models.object import Object
from gmdkit.mappings import obj_prop, obj_id
from gmdkit.utils.id_functions import obj_can_be_spawned

Func = Callable|None

class BaseIdentifier:
    #__slots__ = ('obj','id_val','default','fixed','remappable','remaps')
    
    obj: Object
    obj_prop_id: int|str
    remaps: dict
    id_val: int|tuple[int]
    id_type: str
    id_min: int = -2147483648
    id_max: int = 2147483647
    default: int|None = None
    is_default: bool = False
    remappable: bool = False
    reference: bool = False
    fixed: bool = False
    actions: tuple = tuple()
    iterable: bool = False
    replace: Func = None
    
    
    def __init__(
            self,
            obj:Object,
            id_val:int|tuple[int],
            default:int|None=None,
            fixed:bool=False,
            remappable:bool=False
            ):
        
        self.obj = obj
        self.id_val = id_val
        
        if self.default != default:
            self.default = default
            
        if self.fixed != fixed:
            self.fixed = fixed
        
        if id_val == default:
            if not self.is_default:
                self.is_default = True
            if not self.fixed:
                self.fixed = True
            
        remappable = self.remappable and remappable
        if self.remappable != remappable:
            self.remappable = remappable
        
        if self.remappable:
            self.remaps = dict()
    
    
    def remap_obj(self, kv_map:dict, override:bool=False):
        
        if not override and (self.fixed or self.default) or not kv_map:
            return

        if callable(self.replace):
            val = self.obj.get(self.obj_prop_id)
            if val is not None:
                self.replace(val, kv_map)
            
        elif (new:=kv_map.get(self.val)) is not None:
            self.obj[self.obj_prop_id] = new
        
             
class IDRule:
    
    def __init__(
            self,
            obj_prop_id:int|str,
            id_type:str,
            condition: Func = None,
            function: Func = None,
            fallback: Func = None,
            replace: Func = None,
            fixed: Any = None,
            remappable: Any = None,
            default: Any = None,
            iterable: bool = False,
            reference: bool = False,
            id_min: int = -2147483648,
            id_max: int = 2147483647,
            actions: tuple = tuple()
            ):
        
        d = {}
        
        self.condition = condition
        self.function = function
        self.fallback = fallback
        
        if callable(remappable):
            self.remappable = remappable
        else:
            self.remappable = None
            d["remappable"] = remappable
        
        if callable(default):
            self.default = default
        else:
            self.default = None
            d["default"] = default
            
        if callable(fixed):
            self.fixed = fixed
        else:
            self.fixed = None
            d["fixed"] = fixed
        
        d["obj_prop_id"] = obj_prop_id
        d["id_type"] = id_type
        d["id_min"] = id_min
        d["id_max"] = id_max
        d["reference"] = reference
        d["actions"] = actions
        d["iterable"] = iterable
        d["replace"] = replace
        
        class Identifier(BaseIdentifier):
            for k, v in d.items():
                locals()[k] = v

        self.identifier = Identifier
        

    def get_ids(self, obj:Object):
        i = self.identifier
        pid = i.obj_prop_id
        val = obj.get(pid)
        
        if val is None and callable(self.fallback):
            fb = self.fallback(obj)
            if fb is None:
                return
            val = fb

        if callable(self.condition) and not self.condition(obj): 
            return

        if callable(self.function):
            val = self.function(val)

        if callable(self.default):
            default = self.default(obj)
        else:
            default = i.default
        
        if callable(self.fixed):
            fixed = self.fixed(obj)
        else:
            fixed = i.fixed

        if i.iterable:
            val = tuple(val)
        else:
            val = default
        
        if val is None or len(val)==0: 
            return
        
        yield self.identifier(
            obj=obj,
            id_val=val,
            default=default,
            remappable=obj_can_be_spawned(obj),
            fixed=fixed
        )


class RuleHandler:
    __slots__ = ("base","by_id")
    
    def __init__(self, base:tuple[IDRule], by_id:dict[int|str,tuple[IDRule]]):
        self.base = base or tuple()
        self.by_id = by_id or dict()

    def get_ids(self, obj):
        
        oid = obj.get(obj_prop.ID, obj_id.LEVEL_START)
        
        rules = self.by_id.get(oid)
        if rules is not None:
            for rule in rules:
                yield from rule(obj)
        
        if oid != obj_id.LEVEL_START and self.base:
            for rule in self.base:
                yield from rule(obj)
                
class IdentifierList:
    
    def __init__(self):
        self.ids = list()
        self.ignored = set()
        self.min = -2147483648
        self.max = 2147483647
    
    
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
