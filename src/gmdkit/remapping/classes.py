# Imports
from typing import Callable, Optional, Sequence, Self
from dataclasses import dataclass, field as dc_field
from collections import ChainMap
from functools import lru_cache

# Package Imports
from gmdkit.models.level import Level
from gmdkit.models.object import Object, ObjectList
from gmdkit.serialization.classes import BaseInterface
from gmdkit.remapping.types import IDType, IDActions, AutoID

ID_MIN = -2147483648
ID_MAX =  2147483647


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
    is_default: bool = dc_field(init=False, default=False)

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

    values: tuple[Identifier] = dc_field(default_factory=tuple)
    ignored: set[int] = dc_field(default_factory=set)
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
            ) -> Self:

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

            if has_tags:
                own = i.actions if isinstance(i.actions, tuple) else (i.actions,)
                if not any(t in own for t in has_tags):
                    continue

            result.append(i)

        return self.__class__(values=result)

    def get_ids(
            self,
            in_range:bool = False,
            min_value:Optional[int] = None,
            max_value:Optional[int] = None
            ) -> set:

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
            identifiers: Sequence[Identifier],
            type_groups: Sequence[IDType | Sequence[IDType]] | None = None,
            ):

        id_dict: dict[IDType, list[Identifier]] = {}
        for i in identifiers:
            id_dict.setdefault(i.id_type, []).append(i)

        if type_groups is None:
            return {k: IdentifierList(values=v) for k, v in id_dict.items()}

        seen: set[IDType] = set()
        result: dict[IDType | tuple[IDType, ...], list[Identifier]] = {}

        for k in type_groups:
            if isinstance(k, IDType):  # single type, not a group
                seen.add(k)
                result[k] = id_dict.get(k, [])
            else:
                key = tuple(k)
                seen.update(key)
                result[key] = [v for t in key for v in id_dict.get(t, [])]

        for k in id_dict.keys() - seen:
            result[k] = id_dict[k]

        return {k: IdentifierList(values=v) for k, v in result.items()}


@lru_cache(maxsize=None)
def _property_key(schema: type[BaseInterface], name: str) -> int | str:
    return getattr(schema, name).canonical


@dataclass(slots=True, frozen=True)
class IDRule:
    field: str
    id_type: IDType
    condition: Optional[Callable] = None
    function: Optional[Callable] = None
    fallback: Optional[Callable] = None
    replace: Optional[Callable] = None
    fixed: Optional[Callable|bool] = None
    remappable: Optional[Callable|bool] = None
    when_unset: Callable|bool = False
    iterable: bool = False
    reference: bool = False
    id_min: int = ID_MIN
    id_max: int = ID_MAX
    actions: Optional[tuple] = None

    def key_for(self, schema: type[BaseInterface]) -> int | str:
        return _property_key(schema, self.field)

    def is_matched(
            self,
            id_types: Optional[Sequence[IDType]] = None,
            reference: Optional[bool] = None,
            actions: Optional[Sequence[IDActions]] = None
            ) -> bool:
        if id_types and self.id_type not in id_types:
            return False
        if reference is not None and self.reference != reference:
            return False
        if actions:
            own = self.actions if isinstance(self.actions, tuple) else (self.actions,)
            if not any(a in own for a in actions):
                return False
        return True

    def get_id(self, intf: BaseInterface) -> Optional[Identifier]:
        schema = type(intf)
        val = getattr(intf, self.field)
        has_default = bool(self.when_unset)

        if not val:
            if callable(self.fallback):
                fb = self.fallback(intf)
                if fb is not None:
                    val = fb
            if not val:
                unset = self.when_unset
                if callable(unset):
                    unset = unset(intf)
                if not unset:
                    return

        if callable(self.condition) and not self.condition(intf):
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

        remappable = self.remappable(intf) if callable(self.remappable) else self.remappable
        obj = intf.obj

        return Identifier(
            obj=obj,
            obj_prop_id=self.key_for(schema),
            id_val=val,
            id_type=self.id_type,
            default=0 if has_default else None,
            fixed=bool(fixed),
            remappable=bool(remappable) and bool(getattr(intf, "spawn_trigger", False)),
            reference=self.reference,
            iterable=self.iterable,
            id_min=self.id_min,
            id_max=self.id_max,
            actions=self.actions,
            replace=self.replace,
        )


@dataclass(slots=True)
class RuleHandler:
    rules: dict[type[BaseInterface], dict[IDRule, None]] = dc_field(default_factory=dict)
    groups: Optional[list[Sequence]] = None
    _chains: dict = dc_field(default_factory=dict, repr=False, compare=False)

    def __post_init__(self):
        self.rules = {k: dict.fromkeys(v) for k, v in self.rules.items()}

    def _own(self, klass: type[BaseInterface]) -> dict[IDRule, None]:
        own = self.rules.get(klass)
        if own is None:
            own = self.rules[klass] = {}
        return own

    def chain_for(self, schema: type[BaseInterface]) -> ChainMap:
        chain = self._chains.get(schema)
        if chain is None:
            chain = self._chains[schema] = ChainMap(
                *(self._own(k) for k in schema.__mro__ if issubclass(k, BaseInterface)))
        return chain

    def rules_for(self, schema: type[BaseInterface]) -> tuple[IDRule, ...]:
        return tuple(self.chain_for(schema))

    def register(self, interface: type[BaseInterface], rule: IDRule) -> IDRule:
        try:
            rule.key_for(interface)
        except AttributeError:
            raise AttributeError(
                f"{interface.__name__} has no field {rule.field!r}") from None
        self._own(interface)[rule] = None
        return rule

    def register_rule(
            self,
            interface: type[BaseInterface] | Sequence[type[BaseInterface]],
            field: str,
            id_type: IDType,
            condition: Optional[Callable] = None,
            function: Optional[Callable] = None,
            fallback: Optional[Callable] = None,
            replace: Optional[Callable] = None,
            fixed: Optional[Callable|bool] = None,
            remappable: Optional[Callable|bool] = None,
            when_unset: Callable|bool = False,
            iterable: bool = False,
            reference: bool = False,
            id_min: int = ID_MIN,
            id_max: int = ID_MAX,
            actions: Optional[tuple] = None
            ) -> IDRule:
        rule = IDRule(
            field=field, id_type=id_type, condition=condition, function=function,
            fallback=fallback, replace=replace, fixed=fixed, remappable=remappable,
            when_unset=when_unset, iterable=iterable, reference=reference,
            id_min=id_min, id_max=id_max, actions=actions,
            )
        targets = interface if isinstance(interface, (tuple, list)) else (interface,)
        for target in targets:
            self.register(target, rule)
        return rule

    def compile_rules(self, **kwargs) -> Self:
        filtered = {}
        for klass, own in self.rules.items():
            kept = tuple(r for r in own if r.is_matched(**kwargs))
            if kept:
                filtered[klass] = kept
        return self.__class__(rules=filtered, groups=self.groups)

    def add_groups(self, *groups) -> None:
        current = list(self.groups) if self.groups else []

        for spec in groups:
            if spec:
                current.extend(spec)

        self.groups = current

    def add_rules(self, *handlers: Self) -> Self:
        new = self.__class__()

        for h in (self, *handlers):
            new.add_groups(h.groups)
            for klass, own in h.rules.items():
                new._own(klass).update(own)

        return new

    def fetch_ids(self, obj: Object) -> tuple[Identifier, ...]:
        schema = type(obj).get_schema(obj.current_id)
        rules = self.rules_for(schema)
        if not rules:
            return ()
        intf = schema(obj)
        return tuple(i for r in rules if (i := r.get_id(intf)) is not None)

    def compile_ids(
            self,
            source: ObjectList|Level,
            by_type:bool=False,
            type_groups:Optional[Sequence[set]]=None
            ) -> IdentifierList|dict[Sequence[IDType]|IDType,IdentifierList]:

        result = []
        type_groups = self.groups if type_groups is None else type_groups

        if hasattr(source, "start"):
            result.extend(self.fetch_ids(source.start))

        if hasattr(source, "objects"):
            for obj in source.objects:
                result.extend(self.fetch_ids(obj))

        else:
            for obj in source:
                result.extend(self.fetch_ids(obj))

        if by_type:
            return IdentifierList.group_by_type(result, type_groups)

        return IdentifierList(values=result)