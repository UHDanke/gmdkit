# Imports
from typing import Iterable, Callable, ParamSpec, TypeVar, Optional
import tkinter as tk
from enum import Enum
from functools import lru_cache
import bisect
# Package Imports (only gmdkit.utils is allowed)
from gmdkit.utils.enums import ArrowDir

P = ParamSpec("P")
R = TypeVar("R")

def typed_cache(maxsize=128, typed=False):
    def decorator(f: Callable[P, R]) -> Callable[P, R]:
        return lru_cache(maxsize=maxsize,typed=typed)(f)  # type: ignore
    return decorator

@typed_cache(maxsize=256)
def get_enum_values(cls):
    if not isinstance(cls, Enum):
        raise ValueError(f"expected enum, got {cls.__name__}")
    
    return {e.value for e in cls}       

@typed_cache(maxsize=256)
def normalize_orientation(rotation:float, flip_x:bool=False, flip_y:bool=False):
    rotation = round(rotation%360/90)
    
    match rotation:
        case 0:
            h = ArrowDir.RIGHT
            v = ArrowDir.DOWN
        case 1:
            h = ArrowDir.DOWN
            v = ArrowDir.LEFT
        case 2:
            h = ArrowDir.LEFT
            v = ArrowDir.UP
        case 3:
            h = ArrowDir.UP
            v = ArrowDir.RIGHT
    
    h = h.flip() if flip_x else h
    v = v.flip() if flip_y else v
    
    return h,v


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

class Clipboard:
    
    __slots__ = ("root")
    
    def __init__(self):
        self.root = None
        
    def __enter__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.root.update()
        finally:
            self.root.destroy()
            
    def get(self) -> str:
        try:
            return self.root.clipboard_get()
        except tk.TclError:
            return ""
        
    def set(self, text: str):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        

import time


class Timer:
    
    def __init__(self, start:bool=False, digits:Optional[int]=5):
        self.values = []
        self.paused = True
        self.start_time = 0.0
        self.last_time = 0.0
        self.pause_time = 0.0
        self.digits = digits
        
        if start:
            self.start()
    
    def rounded(self,value):
        d = self.digits
        if d is None:
            return value
        else:
            return round(value, d)
        
    def clear(self):
        self.values.clear()
        self.paused = True
        self.start_time = 0.0
        self.last_time = 0.0
        self.pause_time = 0.0
        
    def start(self) -> float:
        self.clear()
        
        now = time.perf_counter()
        
        self.paused = False
        self.start_time = now
        self.last_time = now
        
        return self.rounded(now)
    
    def end(self) -> float:
        if self.paused:
            return self.values[-1] if self.values else 0.0
            
        value = self.lap()
        self.paused = True
        
        return self.rounded(value)
    
    def pause(self):
        if not self.paused:
            self.pause_time = time.perf_counter()
            self.paused = True
            
    def resume(self):
        if self.paused:
            now = time.perf_counter()
            
            paused_duration = now - self.pause_time
            
            self.start_time += paused_duration
            self.last_time += paused_duration
            
            self.paused = False
            
    def lap(self) -> float:
        if self.paused:
            return 0.0
        
        now = time.perf_counter()
        
        delta = now - self.last_time
        
        self.last_time = now
        self.values.append(delta)
        
        return self.rounded(delta)
    
    def delta(self):
        if self.paused:
            return 0.0
        
        now = time.perf_counter()
        delta = now - self.last_time
        
        return self.rounded(delta)
