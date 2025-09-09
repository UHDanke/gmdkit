# Package Imports
from gmdkit.models.prop.string import GzipString
from gmdkit.models.object import Object, ObjectList


class ObjectString(GzipString):
    
    __slots__ = ()
    
    
    def decompress(self, instance=None):
        
        string = super().decompress()
        
        obj_list = ObjectList.from_string(string)
        
        if obj_list:
            
            start = obj_list.pop(0)
            objects = obj_list
            
            if instance is not None:
                instance.start = start
                instance.objects = objects
            
            return start, objects
        
        return Object(), ObjectList()
    
        
    def compress(self, instance=None, start=None, objects=None):
        
        start = (None if instance is None else getattr(instance, "start", None)) or start
        objects = (None if instance is None else getattr(instance, "objects", None)) or objects
        
        if start is None or objects is None:
            return None
    
        string = (ObjectList(start) + objects).to_string()
        
        return super().compress(string)


class ReplayString(GzipString):
    
    __slots__ = ()
    
    def decompress(self, instance=None):
        
        string = super().decompress()
        
        if instance is not None:
            instance.replay_data = string
            
    def compress(self, instance=None, replay_data=None):
        
        replay_data = (None if instance is None else getattr(instance, "replay_data", None)) or replay_data
        
        if replay_data is None:
            return None
        
        string = replay_data
        
        return super().compress(string)