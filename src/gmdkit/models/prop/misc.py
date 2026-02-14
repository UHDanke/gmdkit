# Package Imports
from gmdkit.models.object import ObjectList
from gmdkit.serialization.mixins import PlistDictDecoderMixin
from gmdkit.serialization.types import DictClass


class ObjectGroup(ObjectList):
    
    __slots__ = ("string")
    
    
    @classmethod
    def from_string(cls, string:str, load:bool=True):
        
        if load:
            new = super().from_string(string)
        else:
            new = cls()
        
        new.string = string
        
        return new
            
        
    def to_string(self, save:bool=True):
        
        if save:
            self.string = super().to_string()
        
        return self.string
    
    
    def load(self):
        self[:] = super().from_string(self.string)
    
    
    def save(self):
        self.string = super().to_string()

    
def _decoder(key, value, load:bool=False, **kwargs):
    return int(key), ObjectGroup.from_string(value,load=load)

def _encoder(key, value, save:bool=False, **kwargs):
    return str(key), ObjectGroup.to_string(value,save=save)


class ObjectGroupDict(PlistDictDecoderMixin,DictClass):
        
    DECODER = staticmethod(_decoder)
    ENCODER = staticmethod(_encoder)
    
    
    def update_index(self):
        items = sorted(self.items())
        self.clear()
        for i, (_, value) in enumerate(items, start=1):
            self[-i] = value