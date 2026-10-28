# Imports
import copy
from typing import Optional, Sequence

# Package Imports
from gmdkit.remapping.types import IDType, IDToken, AutoID, NamedID
from gmdkit.remapping.classes import RuleHandler
from gmdkit.remapping.rules import (
    COPY_ID_HANDLER, REGROUP_ID_HANDLER, BASE_ID_HANDLER, NAMED_ID_HANDLER
    )
from gmdkit.remapping.utils import next_free
from gmdkit.models.level import Level
from gmdkit.models.object import ObjectList
from gmdkit.models import interfaces
from gmdkit.models.prop.named_groups import NameDict, NamedIDList

IDGroup = IDType|Sequence[IDType]
IDRemaps = dict[IDGroup,dict[int,int]]
CompiledIDs = dict

DEFAULT_EXCLUDE = {IDType.ANY:{0}}
NAMED_ORDER_MAX = 500

def offset_object_ids(
        source:ObjectList|Level,
        id_offset:Optional[dict]=None,
        exclude_ids:Optional[dict]=DEFAULT_EXCLUDE,
        rules:RuleHandler=BASE_ID_HANDLER,
        groups:Optional[Sequence[IDGroup]]=None,
        ids:Optional[CompiledIDs]=None
        ) -> IDRemaps:

    exclude_ids = exclude_ids or {}
    id_offset = id_offset or {}
    ig_all = exclude_ids.get(IDType.ANY,set())
    io_all = id_offset.get(IDType.ANY,0)

    remapped = {}

    if ids is None:
        ids = rules.compile_ids(source, by_type=True, type_groups=groups)

    for k,v in ids.items():
        try:
            ig = exclude_ids.get(k,set()) | ig_all
            io = id_offset.get(k,io_all)

            if not io: continue

            old = v.get_ids(in_range=True) - ig

            if not old: continue

            new = {i + io for i in old}

            if any(i < v.vmin or i > v.vmax for i in new):
                raise ValueError("Offset returned out-of-range ID")

            kv_map = dict(zip(old,new))
            v.remap_objects(kv_map)

            remapped[k] = kv_map

        except Exception as e:
            raise RuntimeError(
                f"Offset ID function encountered the following error while processing key {k}:"
                ) from e

    return remapped


def reassign_object_ids(
        source:ObjectList|Level,
        exclude_ids:Optional[dict]=DEFAULT_EXCLUDE,
        id_ranges:Optional[dict]=None,
        reassign_all:bool=False,
        override_fixed:bool=False,
        reassign_auto:bool=False,
        rules:RuleHandler=BASE_ID_HANDLER,
        groups:Optional[Sequence[IDGroup]]=None,
        ids:Optional[CompiledIDs]=None
        ) -> IDRemaps:

    exclude_ids = exclude_ids or {}
    id_ranges = id_ranges or {}
    ig_all = exclude_ids.get(IDType.ANY,set())
    ir_all = id_ranges.get(IDType.ANY,set())

    remapped = {}

    if ids is None:
        ids = rules.compile_ids(source, by_type=True, type_groups=groups)

    for k, v in ids.items():
        try:
            ig = exclude_ids.get(k, set()) | ig_all
            ir = (id_ranges.get(k, set()) | ir_all) - ig

            v = v if override_fixed else v.filter_values(fixed=False)
            used = v.get_ids()
            auto = {x for x in used if type(x) is AutoID}
            used_ints = {x for x in used if not isinstance(x, IDToken)}

            range_search = bool(ir)


            if not reassign_all and not range_search:
                sr = used_ints
                old = set()
                range_min, range_max = v.vmin, v.vmax
            else:
                sr = ir - used_ints

                if not reassign_all:
                    old = used_ints - ig - ir

                else:
                    old = used_ints - ig

                old = {x for x in old if v.vmin <= x <= v.vmax}
                range_min = max(v.vmin, min(ir)) if range_search else v.vmin
                range_max = min(v.vmax, max(ir)) if range_search else v.vmax

            if not (old or reassign_auto and auto):
                continue

            new = next_free(
                sr,
                vmin=range_min,
                vmax=range_max,
                count=len(old)+(len(auto) if reassign_auto else 0),
                in_range=range_search,
            )

            kv_map = dict(zip(sorted(old)+(sorted(auto) if reassign_auto else []),new))
            v.remap_objects(kv_map, override=override_fixed)

            remapped[k] = kv_map

        except Exception as e:
            raise RuntimeError(
                f"Reassign ID function encountered the following error while processing key {k}:"
                ) from e

    return remapped


def resolve_auto_ids(
        source:ObjectList|Level,
        id_ranges:Optional[dict]=None,
        exclude_ids:Optional[dict]=DEFAULT_EXCLUDE,
        rules:RuleHandler=BASE_ID_HANDLER,
        groups:Optional[Sequence[IDGroup]]=None,
        ids:Optional[CompiledIDs]=None
        ) -> IDRemaps:
    
    exclude_ids = exclude_ids or {}
    id_ranges = id_ranges or {}
    ig_all = exclude_ids.get(IDType.ANY,set())
    ir_all = id_ranges.get(IDType.ANY,set())

    remapped = {}

    if ids is None:
        ids = rules.compile_ids(source, by_type=True, type_groups=groups)

    for k, v in ids.items():
        try:

            used = v.get_ids()
            auto = {x for x in used if type(x) is AutoID}
            
            if not auto: continue
        
            used_ints = {x for x in used if not isinstance(x, IDToken)}

            ig = exclude_ids.get(k, set()) | ig_all
            ir = (id_ranges.get(k, set()) | ir_all)
            
            range_search = bool(ir)

            if not range_search:
                sr = used_ints | ig
                range_min, range_max = v.vmin, v.vmax
            else:
                sr = ir - used_ints - ig
                range_min = max(v.vmin, min(ir)) if range_search else v.vmin
                range_max = min(v.vmax, max(ir)) if range_search else v.vmax

            
            new = next_free(
                sr,
                vmin=range_min,
                vmax=range_max,
                count=len(auto),
                in_range=range_search,
            )

            kv_map = dict(zip(sorted(auto),new))
            v.remap_objects(kv_map)

            remapped[k] = kv_map

        except Exception as e:
            raise RuntimeError(
                f"Resolve Auto ID function encountered the following error while processing key {k}:"
                ) from e

    return remapped


def assign_auto_ids(
        source:ObjectList|Level,
        exclude_ids:Optional[dict]=DEFAULT_EXCLUDE,
        override_fixed:bool=False,
        rules:RuleHandler=BASE_ID_HANDLER,
        groups:Optional[Sequence[IDGroup]]=None,
        ids:Optional[CompiledIDs]=None
        ) -> IDRemaps:

    exclude_ids = exclude_ids or {}
    ig_all = exclude_ids.get(IDType.ANY,set())

    remapped = {}

    if ids is None:
        ids = rules.compile_ids(source, by_type=True, type_groups=groups)

    for k, v in ids.items():
        try:
            ig = exclude_ids.get(k, set()) | ig_all

            v = v if override_fixed else v.filter_values(fixed=False)
            used = v.get_ids()
            old = set()
            old = {x for x in used if not isinstance(x, IDToken)} - ig

            if not old: continue

            new = [AutoID() for _ in old]

            kv_map = dict(zip(sorted(old),new))

            v.remap_objects(kv_map, override=override_fixed)

            remapped[k] = kv_map

        except Exception as e:
            raise RuntimeError(
                f"Reassign ID function encountered the following error while processing key {k}:"
                ) from e

    return remapped


def remap_objects(
        *sources:ObjectList|Level,
        rules:RuleHandler,
        groups:Optional[Sequence[Sequence[IDType]]]=None,
        ref_groups:Optional[Sequence[Sequence[IDType]]]=None,
        override_fixed:bool=False,
        exclude_ids:Optional[dict]=DEFAULT_EXCLUDE,
        include_ids:Optional[dict]=None,
        ) -> list[ObjectList|Level]:

    exclude_ids = exclude_ids or {}
    include_ids = include_ids or {}
    ig_all = exclude_ids.get(IDType.ANY, set())
    ig_dict = {k: v | ig_all for k, v in exclude_ids.items()}

    ic_all = include_ids.get(IDType.ANY, set())
    ic_dict = {}
    ia_dict = {}
    for k, v in include_ids.items():
        ic_dict[k] = v | ic_all | ig_dict.get(k, set())
        ia_dict[k] = {x for x in ic_dict[k] if type(x) is AutoID}

    ref_groups = () if ref_groups is None else ref_groups
    result = []
    last_ids = {}

    for s in sources:
        s = copy.deepcopy(s)
        result.append(s)
        ids = rules.compile_ids(s, by_type=True, type_groups=groups)

        for k, v in ids.items():
            ig = ig_dict.setdefault(k, set(ig_all))
            ic = ic_dict.setdefault(k, ic_all | ig)
            ia = ia_dict.setdefault(k, {x for x in ic if type(x) is AutoID})

            used = v.get_ids()
            used_auto = {x for x in used if type(x) is AutoID}
            v = v if override_fixed else v.filter_values(fixed=False)

            if k in ref_groups:
                id_base = v.filter_values(reference=False).get_ids()
                id_ref = v.filter_values(reference=True).get_ids()
                coll = (ic & id_base & id_ref) - ig
            else:
                av = used if override_fixed else v.get_ids()
                coll = (ic & av) - ig

            ic.update(used)
            ia.update(used_auto)

            coll = {x for x in coll if type(x) is not NamedID}

            if not coll: continue

            coll_auto = {x for x in coll if type(x) is AutoID}
            coll_ints = coll - coll_auto

            new_ints = next_free(
                {x for x in ic if not isinstance(x, IDToken)},
                start=last_ids.get(k),
                vmin=v.vmin,
                vmax=v.vmax,
                count=len(coll_ints),
            ) if coll_ints else []

            if new_ints:
                last_ids[k] = new_ints[-1]

            new_auto = [AutoID() for _ in coll_auto]

            kv_map = {**dict(zip(sorted(coll_ints), new_ints)), **dict(zip(sorted(coll_auto), new_auto))}
            v.remap_objects(kv_map, override=override_fixed)
            ic.update(new_ints)
            ic.update(new_auto)
            ia.update(new_auto)

    return result


def remap_objects_copy(
        *sources:ObjectList|Level,
        rules:RuleHandler=COPY_ID_HANDLER
        ) -> list[ObjectList|Level]:

    return remap_objects(
        *sources,
        rules=rules
        )


def remap_objects_regroup(
        *sources:ObjectList|Level,
        exclude_ids:Optional[dict]=DEFAULT_EXCLUDE,
        include_ids:Optional[dict]=None,
        override_fixed:bool=False,
        rules:RuleHandler=REGROUP_ID_HANDLER,
        groups:Optional[Sequence[Sequence[IDType]]]=None,
        ref_groups:Optional[Sequence[Sequence[IDType]]]=None
        ) -> list[ObjectList|Level]:

    return remap_objects(
        *sources,
        rules=rules,
        groups=groups,
        ref_groups=ref_groups,
        exclude_ids=exclude_ids,
        include_ids=include_ids,
        override_fixed=override_fixed
        )


def remap_objects_build_helper(
        *sources:ObjectList|Level,
        exclude_ids:Optional[dict]=DEFAULT_EXCLUDE,
        include_ids:Optional[dict]=None,
        override_fixed:bool=False,
        rules:RuleHandler=REGROUP_ID_HANDLER,
        groups:Optional[Sequence[Sequence[IDType]]]=None,
        ref_groups:Optional[Sequence[Sequence[IDType]]]=None
        ) -> list[ObjectList|Level]:

    if ref_groups is None:
        ref_groups = rules.groups if groups is None else groups

    return remap_objects(
        *sources,
        rules=rules,
        groups=groups,
        ref_groups=ref_groups,
        exclude_ids=exclude_ids,
        include_ids=include_ids,
        override_fixed=override_fixed
        )


def combine_objects(
        *sources:ObjectList|Level
        ) -> ObjectList|Level:

    result = sources[0]
    main_level = issubclass(type(result), Level)

    if main_level:
        objects = result.objects
        start_intf = result.start.require_interface(interfaces.LevelSettings)
        colors = start_intf.colors
    else:
        objects = result

    for i in sources[1:]:
        if not issubclass(type(i), Level):
            objects.extend(i)
        else:
            objects.extend(i.objects)
            if main_level:
                iintf = i.start.require_interface(interfaces.LevelSettings)
                col = iintf.colors
                if col is not None:
                    colors.add_colors(col)
                combine_named_groups(start_intf, iintf)

    return result


def combine_named_groups(
        target:interfaces.LevelSettings,
        source:interfaces.LevelSettings
        ) -> list[tuple]:

    conflicts = []
    target_named = target.named_groups

    for key, names in source.named_groups.items():
        if not names: continue
        target_names = target_named.setdefault(key, NameDict())
        for i, name in names.items():
            current = target_names.get(i)
            if current is None:
                target_names[i] = name
            elif current != name:
                conflicts.append((key, i, current, name))

    target_order = target.named_groups_order

    for key, ids in source.named_groups_order.items():
        named = target_named.get(key)
        if not ids or not named: continue
        order = target_order.setdefault(key, NamedIDList())
        seen = set(order)
        for i in ids:
            if i in named and i not in seen:
                order.append(i)
                seen.add(i)
        del order[NAMED_ORDER_MAX:]

    return conflicts


def assign_named_ids(
        source:Level,
        rules:RuleHandler=NAMED_ID_HANDLER,
        ids:Optional[CompiledIDs]=None
        ) -> IDRemaps:

    named = source.start.require_interface(interfaces.LevelSettings).named_groups
    if not named:
        return {}

    if ids is None:
        ids = rules.compile_ids(source, by_type=True, type_groups=(), include_unset=False)

    remapped = {}

    for k, v in ids.items():
        if not isinstance(k, IDType): continue

        names = named.get(k.to_named_type())
        if not names: continue

        kv_map = {i: NamedID(names[i]) for i in v.get_ids() if i in names}
        if not kv_map: continue

        v.remap_objects(kv_map)
        remapped[k] = kv_map

    return remapped


def resolve_named_ids(
        source:Level,
        exclude_ids:Optional[dict]=DEFAULT_EXCLUDE,
        register:bool=True,
        rules:RuleHandler=NAMED_ID_HANDLER,
        ids:Optional[CompiledIDs]=None
        ) -> IDRemaps:

    exclude_ids = exclude_ids or {}
    ig_all = exclude_ids.get(IDType.ANY, set())
    settings = source.start.require_interface(interfaces.LevelSettings)
    named = settings.named_groups
    order = settings.named_groups_order

    if ids is None:
        ids = rules.compile_ids(source, by_type=True, type_groups=(), include_unset=False)

    remapped = {}

    for k, v in ids.items():
        used = v.get_ids()
        tokens = {x for x in used if type(x) is NamedID}
        if not tokens: continue

        if not isinstance(k, IDType):
            raise ValueError(f"named IDs cannot be resolved for the grouped key {k!r}")

        key = k.to_named_type()

        names = named.setdefault(key, NameDict()) if register else named.get(key, {})
        by_name = {}
        for i in sorted(names):
            by_name.setdefault(names[i], i)

        kv_map = {t: by_name[t.name] for t in tokens if t.name in by_name}
        missing = sorted(t for t in tokens if t.name not in by_name)

        if missing and not register:
            raise KeyError(f"undefined {k.name} names: {[t.name for t in missing]}")

        if missing:
            used_ints = {x for x in used if not isinstance(x, IDToken)}
            taken = used_ints | set(names) | exclude_ids.get(k, set()) | ig_all
            new = next_free(taken, vmin=max(v.vmin, 1), vmax=v.vmax, count=len(missing))
            ids_order = order.setdefault(key, NamedIDList())

            for token, i in zip(missing, new):
                kv_map[token] = i
                names[i] = token.name
                if i not in ids_order:
                    ids_order.insert(0, i)

            del ids_order[NAMED_ORDER_MAX:]

        v.remap_objects(kv_map)
        remapped[k] = kv_map

    return remapped