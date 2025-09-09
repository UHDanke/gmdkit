# Imports
from pathlib import Path
from os import PathLike, getenv

# Package Imports
from gmdkit.models.level import Level, LevelList
from gmdkit.models.types import ListClass, DictClass
from gmdkit.models.serialization import decode_save, encode_save, from_plist_string, to_plist_string


LOCALPATH = Path(getenv("LOCALAPPDATA")) / "GeometryDash"


class LevelSave(DictClass):
    
    __slots__ = ("path")
    
    def __init__(self, path:str|PathLike=None, load_levels:bool=True, lazy_load:bool=True):
        
        if path is None:
            path = LOCALPATH / "CCLocalLevels.dat"
            
        self.path = path
        
        if load_data:
            self.load(lazy_load=lazy_load)
    
    
    def load(self, lazy_load:bool=True):
        
        with open(self.path,"r") as file:
            string = decode_save(file.read())
            data = from_plist_string(string)
            
            data["LLM_01"] = LevelList([Level(x,lazy_load=lazy_load) for x in data["LLM_01"]])
            data["LLM_03"] = LevelList([Level(x,lazy_load=True) for x in data["LLM_03"]])
            
            self.levels = data["LLM_01"]
            self.binary = data["LLM_02"]
            self.lists = data["LLM_03"]
            
            super().__init__(data)   
    
    def save(self,path:str|PathLike=None):
        
        if path is None: path = self.path
        
        for level in self.levels:
            level.save()
            
        for lst in self.lists:
            lst.save()
        
        data["LLM_01"] = self.levels
        data["LLM_02"] = self.binary
        data["LLM_03"] = self.lists
        
        with open(path, "w") as file:
            string = to_plist_string(self)
            encoded = encode_save(string)
            file.write(encoded)
    
    
            
            
if __name__ == "__main__":
    level_data = LevelSave()
    levels = level_data.levels
    binary = level_data.binary
    lists = level_data.lists
    