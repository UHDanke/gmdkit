# Imports
from typing import TypeVar, Optional, Any, Generic, overload
import tkinter as tk
import time


T = TypeVar("T")

class ObjField(Generic[T]):
    def __init__(self, key: Any) -> None:
        self.key = key

    @overload
    def __get__(self, instance: None, owner: type[Any]) -> "ObjField[T]": ...
    @overload
    def __get__(self, instance: object, owner: type[Any] | None = None) -> T: ...
    def __get__(self, instance: object | None, owner: type[Any] | None = None) -> T | "ObjField[T]":
        if instance is None:
            return self
        return instance.obj[self.key] # type: ignore[attr-defined]

    def __set__(self, instance: Any, value: T) -> None:
        instance.obj[self.key] = value
        
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
