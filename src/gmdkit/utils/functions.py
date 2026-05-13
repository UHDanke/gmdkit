# Imports
from typing import Callable, ParamSpec, TypeVar
from enum import Enum
from functools import lru_cache, partial
from inspect import signature

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