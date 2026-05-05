# Imports
from typing import Iterable, Callable, ParamSpec, TypeVar, Optional
import tkinter as tk
from enum import Enum
from functools import lru_cache

# Package Imports (only gmdkit.utils is allowed)
from gmdkit.utils.enums import ArrowDir

P = ParamSpec("P")
R = TypeVar("R")

def typed_cache(maxsize=128, typed=False):
    def decorator(f: Callable[P, R]) -> Callable[P, R]:
        return lru_cache(maxsize=maxsize,typed=typed)(f)  # type: ignore
    return decorator


class Clipboard:
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


@typed_cache(maxsize=256)
def get_enum_values(cls):
    if not isinstance(cls, Enum):
        raise ValueError(f"expected enum, got {cls.__name__}")
    
    return {e.value for e in cls}

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
    result = []

    def range_search(start: int, stop: int, step: int):
        nonlocal result
        i = start
        while (i < stop if step > 0 else i > stop):
            if len(result) >= count:
                break
            if (i in values) == in_range:
                result.append(i)
            i += step


    if vmin > vmax: return result
    if start is None:
        start = 1 if vmin <= 0 else vmin
    else:
        if start < vmin:
            start = vmin
        elif start > vmax:
            start = 0 if vmin < 0 else vmax
        
    if start is not None and start <= vmax:
        range_search(start, vmax+1, 1)

    if len(result) < count and start is not None and start >= vmin:
        range_search(start, vmin-1, -1)
    
    return result
    