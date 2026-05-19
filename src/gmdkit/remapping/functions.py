# Imports
import copy
from typing import Callable, Optional, Sequence

# Package Imports
from gmdkit.remapping.types import IDType, AutoID
from gmdkit.remapping.classes import RuleHandler
from gmdkit.remapping.rules import (
    COPY_ID_HANDLER, REGROUP_ID_HANDLER, BASE_ID_HANDLER,
    REGROUP_IDS
    )
from gmdkit.models.level import Level
from gmdkit.models.object import ObjectList
from gmdkit.models.prop.color import ColorList
from gmdkit.mappings import obj_prop
from gmdkit.remapping.utils import next_free
from gmdkit.functions.object import clean_duplicate_groups
from gmdkit.functions.object_list import clean_gid_parents


def offset_object_ids(
        source:ObjectList|Level,
        id_offset:Optional[dict]=None,
        ignore_ids:Optional[dict]=None,
        rules:RuleHandler=BASE_ID_HANDLER,
        groups:Optional[Sequence[Sequence[IDType]]]=None
        ):
    
    ignore_ids = ignore_ids or {}
    id_offset = id_offset or {}
    ig_all = ignore_ids.get(IDType.ANY,set())
    io_all = id_offset.get(IDType.ANY,0)
    
    ids = rules.compile_ids(source, by_type=True, type_groups=groups)
    
    for k,v in ids.items():
        try:
            ig = ignore_ids.get(k,set()) | ig_all
            io = id_offset.get(k,io_all)
            
            if not io: continue
            
            old = v.get_ids(in_range=True) - ig
            
            if not old: continue
            
            new = {i + io for i in old}
    
            if any(i < v.vmin or i > v.vmax for i in new):
                raise ValueError("Offset returned out-of-range ID")
                    
            kv_map = dict(zip(old,new))
            v.remap_objects(kv_map)
        except Exception as e:
            raise RuntimeError(
                f"Offset ID function encountered the following error while processing key {k}:"
                ) from e
        
    return source


def reassign_object_ids(
        source:ObjectList|Level,
        ignore_ids:Optional[dict]=None,
        id_ranges:Optional[dict]=None,
        reassign_all:bool=False,
        override_fixed:bool=False,
        rules:RuleHandler=BASE_ID_HANDLER,
        groups:Optional[Sequence[Sequence[IDType]]]=None
        ):
    
    ignore_ids = ignore_ids or {}
    id_ranges = id_ranges or {}
    ig_all = ignore_ids.get(IDType.ANY,set())
    ir_all = id_ranges.get(IDType.ANY,set())
    
    ids = rules.compile_ids(source, by_type=True, type_groups=groups)
    
    for k, v in ids.items():
        try:
            ig = ignore_ids.get(k, set()) | ig_all
            ir = (id_ranges.get(k, set()) | ir_all) - ig
        
            v = v if override_fixed else v.filter_values(fixed=False)
            used = v.get_ids()
            old = set()
            auto = {x for x in used if type(x) is AutoID}
            used_ints = used - auto
        
            range_search = bool(ir)
            
        
            if not reassign_all and not range_search:
                sr = used_ints
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
            
            if not (old or auto): continue
        
            new = next_free(
                sr,
                vmin=range_min,
                vmax=range_max,
                count=len(old)+len(auto),
                in_range=range_search,
            )
                    
            kv_map = dict(zip(sorted(old)+sorted(auto),new))
            
            v.remap_objects(kv_map, override=override_fixed)
        except Exception as e:
            raise RuntimeError(
                f"Reassign ID function encountered the following error while processing key {k}:"
                ) from e
    return source


def resolve_auto_ids(
        source:ObjectList|Level,
        rules:RuleHandler=BASE_ID_HANDLER,
        groups:Optional[Sequence[Sequence[IDType]]]=None
        ):
    
    return reassign_object_ids(
            source=source,
            rules=rules,
            groups=groups
            )
    

def assign_auto_ids(
        source:ObjectList|Level,
        ignore_ids:Optional[dict]=None,
        reassign_all:bool=False,
        override_fixed:bool=False,
        rules:RuleHandler=BASE_ID_HANDLER,
        groups:Optional[Sequence[Sequence[IDType]]]=None
        ):
    
    ignore_ids = ignore_ids or {}
    ig_all = ignore_ids.get(IDType.ANY,set())
    
    ids = rules.compile_ids(source, by_type=True, type_groups=groups)
    
    for k, v in ids.items():
        try:
            ig = ignore_ids.get(k, set()) | ig_all
        
            v = v if override_fixed else v.filter_values(fixed=False)
            used = v.get_ids()
            old = set()
            auto = {x for x in used if type(x) is AutoID}
            old = used - auto - ig

            if not old: continue
        
            new = [AutoID() for _ in old]
                    
            kv_map = dict(zip(sorted(old),new))
            
            v.remap_objects(kv_map, override=override_fixed)
        except Exception as e:
            raise RuntimeError(
                f"Reassign ID function encountered the following error while processing key {k}:"
                ) from e
    return source


def remap_objects(
        *sources: ObjectList | Level,
        rules: RuleHandler,
        groups: Optional[Sequence[Sequence[IDType]]] = None,
        ref_groups: Optional[Sequence[Sequence[IDType]]] = None,
        override_fixed: bool = False,
        ignore_ids: Optional[dict] = None,
        include_ids: Optional[dict] = None,
        ) -> list:

    ignore_ids = ignore_ids or {}
    include_ids = include_ids or {}
    ig_all = ignore_ids.get(IDType.ANY, set())
    ig_dict = {k: v | ig_all for k, v in ignore_ids.items()}

    ic_all = include_ids.get(IDType.ANY, set())
    ic_dict = {}
    ia_dict = {}
    for k, v in include_ids.items():
        ic_dict[k] = v | ic_all | ig_dict.get(k, set())
        ia_dict[k] = {x for x in ic_dict[k] if type(x) is AutoID}

    groups = () if groups is None else groups
    ref_groups = () if ref_groups is None else ref_groups
    result = []
    last_ids = {}

    for s in sources:
        s = copy.deepcopy(s)
        result.append(s)
        ids = rules.compile_ids(s, by_type=True, type_groups=groups)

        for k, v in ids.items():
            ic = ic_dict.setdefault(k, set())
            ia = ia_dict.setdefault(k, set())
            ig = ig_dict.setdefault(k, set())

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

            if not coll: continue
        
            coll_auto = {x for x in coll if type(x) is AutoID}
            coll_ints = coll - coll_auto

            new_ints = next_free(
                ic - ia,
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
        *sources:ObjectList,
        rules:RuleHandler=COPY_ID_HANDLER
        ):
    
    return remap_objects(
        *sources,
        rules=rules
        )


def remap_objects_regroup(
        *sources:ObjectList|Level, 
        ignore_ids:Optional[dict]=None, 
        include_ids:Optional[dict]=None,
        override_fixed:bool=False,
        rules:RuleHandler=REGROUP_ID_HANDLER,
        groups:Optional[Sequence[Sequence[IDType]]]=REGROUP_IDS,
        ref_groups:Optional[Sequence[Sequence[IDType]]]=None
        ):
            
    return remap_objects(
        *sources, 
        rules=rules, 
        groups=groups, 
        ref_groups=ref_groups,
        ignore_ids=ignore_ids,
        include_ids=include_ids,
        override_fixed=override_fixed
        )


def remap_objects_build_helper(
        *sources:ObjectList, 
        ignore_ids:Optional[dict]=None, 
        include_ids:Optional[dict]=None,
        override_fixed:bool=False,
        rules:RuleHandler=REGROUP_ID_HANDLER,
        groups:Optional[Sequence[Sequence[IDType]]]=REGROUP_IDS,
        ref_groups:Optional[Sequence[Sequence[IDType]]]=None
        ):
    
    ref_groups = groups if ref_groups is None else ref_groups
    
    return remap_objects(
        *sources, 
        rules=rules, 
        groups=groups, 
        ref_groups=ref_groups,
        ignore_ids=ignore_ids,
        include_ids=include_ids,
        override_fixed=override_fixed
        )


def combine_objects(
        *sources:ObjectList|Level,
        remap_func:Optional[Callable]=None,
        **func_kwargs
        ):
    
    if remap_func is not None:
        sources = remap_func(*sources, **func_kwargs)
    
    result = sources[0]
    main_level = issubclass(type(result), Level)
    
    if main_level:
        objects = result.objects
        colors = result.start.get(obj_prop.level.COLORS, ColorList())
    else:
        objects = result
    
    for i in sources[1:]:
        if not issubclass(type(i), Level):
            objects.extend(i)
        else:
            objects.extend(i.objects)
            if main_level:
                col = i.start.get(obj_prop.level.COLORS)
                if col is not None:  
                    colors.add_colors(col)
    
    objects.apply(clean_duplicate_groups)
    clean_gid_parents(objects)
    
    return result


