# Imports
from typing import Optional

# Package Imports
from gmdkit.models.object import Object, ObjectList
from gmdkit.serialization.mixins import FileStringMixin
from gmdkit.serialization.functions import decompress_string, compress_string
from gmdkit.models.prop.replay import ReplayInfo, ReplayEvents


class GzipString(FileStringMixin):

    def __init__(self, string: Optional[str] = None):
        self.string = string or ""
        self.decompressed: Optional[str] = None

    def load(self) -> str:
        self.decompressed = decompress_string(self.string)
        return self.decompressed

    def save(self, string: Optional[str] = None) -> None:
        if string is not None:
            self.decompressed = string
        
        if self.decompressed is not None:
            self.string = compress_string(self.decompressed)

    @classmethod
    def from_string(cls, string: str, load: bool = True):
        new = cls(string)

        if load:
            new.load()

        return new

    def to_string(self, save: bool = True):
        if save:
            self.save()

        return self.string
    

class ObjectString(GzipString):
    
    def load(
            self, string:Optional[str]=None, 
            compressed:bool=True
            ) -> tuple[Object,ObjectList]:
        
        if string is None:
            string = super().load()
        elif compressed:
            string = decompress_string(string)
            
        first, _, remainder = string.partition(";")
        
        self.start = Object.from_string(first)
        self.objects = ObjectList.from_string(remainder)
    
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
        
        replay_string, replay_start = string.split("#", 1)
        
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