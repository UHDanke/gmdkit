# Package Imports
from typing import Any
from gmdkit.models.object import Object, ObjectList
from gmdkit.serialization.functions import decode_string, encode_string


class GzipString:
    
    __slots__ = ("string")
    
    def __init__(self, string:str=""):
        self.string = string
    
    def load(self) -> str:
        return decode_string(self.string)

    def save(self, string:str) -> None:
        self.string = encode_string(string)
        

class ObjectString(GzipString):
    
    def load(self, string:str|None=None):
        
        string = string if string is not None else super().load()
        
        obj_list = ObjectList.from_string(string)
        
        if obj_list:
            
            self.start = obj_list.pop(0)
            self.objects = obj_list
        
        return Object(), ObjectList()
    
        
    def save(self, start:Object|None=None, objects:ObjectList|None=None):
        
        start = start or getattr(self, "start", None)
        objects =  objects or getattr(self, "objects", None)
        
        if start is None or objects is None:
            return self.string
    
        string = (ObjectList().wrap(start) + objects).to_string()
        
        return super().save(string)


class ReplayString(GzipString):
    
    def load(self, instance: Any = None):
        
        string = super().load()
        
        self.replay_data = string
            
    def save(self, replay_data: str | None = None):
        
        replay_data = replay_data or getattr(self, "replay_data", None)
        
        if replay_data is None:
            return self.string
        
        string = replay_data
        
        return super().save(string)