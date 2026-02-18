# Imports
from typing import Optional

# Package Imports
from gmdkit.models.object import Object, ObjectList
from gmdkit.serialization.functions import decompress_string, compress_string


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
        
        self.replay_data = string
            
    def save(self, replay_data: Optional[str]=None):
        
        replay_data = replay_data or getattr(self, "replay_data", None)
        
        if replay_data is None:
            return self.string
        
        string = replay_data
        
        super().save(string)
        
        return self.string