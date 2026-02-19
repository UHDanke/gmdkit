# Imports
from typing import Optional

# Package Imports
from gmdkit.models.object import Object, ObjectList
from gmdkit.serialization.functions import decompress_string, compress_string
from gmdkit.models.prop.replay_data.replay import ReplayInfo, ReplayEvents

class GzipString:
        
    def __init__(self, string:Optional[str]=None):
        self.string = string or str()
    
    def load(self) -> str:
        return decompress_string(self.string)

    def save(self, string:str) -> None:
        self.string = compress_string(string)
        

class ObjectString(GzipString):
    
    def load(
            self, string:Optional[str]=None, 
            compressed:bool=True
            ) -> tuple[Object,ObjectList]:
        
        if string is None:
            string = super().load()
        elif compressed:
            string = decompress_string(string)
        
        obj_list = ObjectList.from_string(string)
        
        if obj_list:
            self.start = obj_list[0]
            self.objects = obj_list[1:]
        else:
            self.start = Object()
            self.objects = ObjectList()
        
        return (self.start, self.objects)
    
    def save(
            self,
            start: Optional[Object]=None,
            objects: Optional[ObjectList]=None,
            ) -> str:
        start = start if start is not None else getattr(self, "start", None)
        objects = objects if objects is not None else getattr(self, "objects", None)
    
        if start is None or objects is None:
            return self.string
    
        string = start.to_string() + objects.to_string()
        super().save(string)
        return self.string
    

class ReplayString(GzipString):
    
    def load(self):
        
        string = super().load()
        
        replay_string, replay_start = string.split("#")
        print(replay_start)
        self.start = ReplayInfo.from_string(replay_start)
        self.events = ReplayEvents.from_string(replay_string)
            
    def save(
            self,
            start: Optional[ReplayInfo]=None,
            events: Optional[ReplayEvents]=None,
            ) -> str:
        
        start = start if start is not None else getattr(self, "start", None)
        events = events if events is not None else getattr(self, "events", None)
        
        if start is None or events is None:
            return self.string
        
        string = start.to_string() + events.to_string()
        
        super().save(string)
        
        return self.string