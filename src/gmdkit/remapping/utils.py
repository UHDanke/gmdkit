# Imports
import re
import bisect
from typing import Callable, Optional, Iterable

# Package Imports
from gmdkit.mappings import obj_prop
from gmdkit.remapping.classes import IDType, IDRule


def create_text_rule(
        regex:str,
        id_type:IDType,
        condition:Optional[Callable]=None,
        id_min:Optional[int]=None,
        id_max:Optional[int]=None
        ) -> IDRule:
    # Compiles an ID rule that retrieves a group ID from a text object field.
    
    pattern = re.compile(regex)
    
    def function(text: str):
        match = pattern.search(text)
        if not match:
            return None
        return int(match.group(1) if match.lastindex else match.group(0))
    
    def replace(text: str, new_id: int):
        match = pattern.search(text)
        if not match:
            return text
        return text[:match.start(1)] + str(new_id) + text[match.end(1):] if match.lastindex else str(new_id)
    
    optionals = {}
    if condition is not None:
        optionals["condition"] = condition
    if id_min is not None:
        optionals["id_min"] = id_min
    if id_max is not None:
        optionals["id_max"] = id_max
         
    return IDRule(
        obj_prop_id=obj_prop.text.DATA,
        id_type=id_type,
        function=function,
        replace=replace,
        **optionals
    )


def next_free(
        values:Iterable[int],
        start:Optional[int]=None,
        vmin:int=-2**31,
        vmax:int=2**31-1,
        count:int=1,
        in_range:bool=False
        ) -> list[int]:
    """
    Returns the next unused integer from a list, within the given limits.
    Negative numbers are returned counting down from -1.

    Parameters
    ----------
    values : Iterable[int]
        Currently used values.
        
    start : int, optional
        The current next free value, used to speed up iterative searches over large lists. Defaults to 0.
    
    vmin : int, optional
        The minimum value that can be returned. Defaults to -inf.
    
    vmax : int, optional
        The maximum value that can be returned. Defaults to inf.
    
    count : int, optional
        The number of values to return. Defaults to 1.
        
    in_range : bool, optional
        Whether to return integers from values (True) or not part of values (False)
        
    Returns
    -------
    new_ids : list[int]
        A list of ids returned.
    """
    if vmin > vmax or count == 0:
        return ()

    if start is None:
        start = 0 if vmin <= 0 else vmin
    else:
        start = max(vmin, min(vmax, start))
        
    if isinstance(values, (set, frozenset)):
        values = sorted(values) if in_range else values
    else :
        values = sorted(set(values)) if in_range else set(values)

    if count == 1:
        if in_range:
            idx = bisect.bisect_left(values, start)
            if idx < len(values) and values[idx] <= vmax:
                return (values[idx],)
            if start > vmin:
                idx = bisect.bisect_left(values, vmin)
                end = bisect.bisect_right(values, start - 1)
                if idx < end:
                    return (values[idx],)
        else:
            for i in range(start, vmax + 1):
                if i not in values:
                    return (i,)
            for i in range(start - 1, vmin - 1, -1):
                if i not in values:
                    return (i,)
        raise ValueError("Range has no valid ID")
        
    result = []

    def scan_sorted(lo: int, hi: int) -> None:
        if lo > hi or len(result) >= count:
            return
        idx_lo = bisect.bisect_left(values, lo)
        idx_hi = bisect.bisect_right(values, hi)
        needed = count - len(result)
        result.extend(values[idx_lo:idx_lo + min(idx_hi - idx_lo, needed)])

    def scan_set(lo: int, hi: int) -> None:
        if lo > hi or len(result) >= count:
            return
        needed = count - len(result)
        for i in range(lo, hi + 1):
            if i not in values:
                result.append(i)
                needed -= 1
                if needed == 0:
                    return

    scan = scan_sorted if in_range else scan_set

    scan(start, vmax)
    if len(result) < count:
        scan(vmin, start - 1)
    l = len(result)
    
    if not l:
        raise ValueError("Range has no valid ID")
    elif l < count:
        raise ValueError(f"Could only retrieve {len(result)} ids out of {count} from range")

    return tuple(result)