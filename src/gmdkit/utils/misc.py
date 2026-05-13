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
