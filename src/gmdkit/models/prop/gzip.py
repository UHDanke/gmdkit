# Package Imports
from gmdkit.models.prop.string import GzipString
from gmdkit.models.object import Object, ObjectList


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
            return None
    
        string = (ObjectList((start,)) + objects).to_string()
        
        return super().save(string)


class ReplayString(GzipString):
    
    def load(self, instance=None):
        
        string = super().load()
        
        self.replay_data = string
            
    def save(self, replay_data=None):
        
        replay_data = replay_data or getattr(self, "replay_data", None)
        
        if replay_data is None:
            return None
        
        string = replay_data
        
        return super().save(string)