# Imports
import math
from typing import Callable, ParamSpec, TypeVar, get_type_hints
from enum import Enum
from functools import lru_cache, partial
from inspect import signature
import random
import string as strlib

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
def cached_type_hints(cls):
    return get_type_hints(cls)

def filter_kwargs(*functions:Callable, **kwargs) -> list[Callable]:
    """
    Filters keyword arguments to only those present on the given functions.
    
    Parameters
    ----------
    *functions : Callable
        One or more functions to retrieve the parameters from.
        
    **kwargs : dict[str,Any]
        The keyword arguments to filter.
        
    Returns
    -------
    funcs : list[Callable]
        A list containing functions with embedded kwargs.
        
    """
    if not kwargs: 
        return functions
    kw_keys = set(kwargs)
    result = []
    
    for fn in functions:
        params = signature(fn).parameters
        if params:
            kw = {k: kwargs[k] for k in kw_keys & set(params)}
            if kw:
                result.append(partial(fn, **kw))
            else:
                result.append(fn)
        else:
            result.append(fn)
    
    return result

def node_matrix(scale_x: float, scale_y: float, rotation_x: float, rotation_y: float,
                flip_x: bool = False, flip_y: bool = False) -> tuple[float, float, float, float]:
    if flip_x:
        scale_x = -scale_x
    if flip_y:
        scale_y = -scale_y
    radians_x = -math.radians(rotation_x)
    radians_y = -math.radians(rotation_y)
    return (
        math.cos(radians_y) * scale_x,
        math.sin(radians_y) * scale_x,
        -math.sin(radians_x) * scale_y,
        math.cos(radians_x) * scale_y,
    )

def transform_corners(half_w: float, half_h: float, center: tuple[float, float],
                      matrix: tuple[float, float, float, float]) -> list[tuple[float, float]]:
    a, b, c, d = matrix
    cx, cy = center
    return [(cx + a * px + c * py, cy + b * px + d * py)
            for px, py in ((-half_w, -half_h), (half_w, -half_h), (half_w, half_h), (-half_w, half_h))]

def bounds(points: list[tuple[float, float]]) -> tuple[float, float, float, float]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)

def create_uid(length:int=16):
    uid_chars = strlib.digits + strlib.ascii_uppercase + strlib.ascii_lowercase
    return "".join(random.choices(uid_chars, k=length))