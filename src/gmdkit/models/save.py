# Imports
from pathlib import Path
from os import PathLike, getenv
from collections.abc import Iterable

# Package Imports
from gmdkit.models.level import Level, LevelList
from gmdkit.models.level_pack import LevelPack, LevelPackList
from gmdkit.models.types import ListClass, DictClass
from gmdkit.models.serialization import PlistDictDecoderMixin, dict_cast, decode_save, encode_save


LOCALPATH = Path(getenv("LOCALAPPDATA")) / "GeometryDash"
LOCALLEVELSPATH = LOCALPATH / "CCLocalLevels.dat"
GAMEMANAGERPATH = LOCALPATH / "CCGameManager.dat"


class LevelSave(PlistDictDecoderMixin, DictClass):
    
    DECODER = staticmethod(dict_cast({"LLM_01": LevelList.from_plist,"LLM_03": LevelPackList.from_plist}))   
    ENCODER = staticmethod(lambda x, **kwargs: x.to_plist(**kwargs))
    
    @classmethod
    def from_file(cls, path:str|PathLike=LOCALLEVELSPATH, encoded:bool=True, **kwargs):
                    
        with open(path, "r") as file:
            
            string = file.read()
            
            if encoded: string = decode_save(string)
            
            return super().from_string(string, **kwargs)
    
    
    @classmethod
    def to_file(self, path:str|PathLike=LOCALLEVELSPATH, encoded:bool=True, **kwargs):
                    
        with open(path, "w") as file:
            
            string = super().to_string(**kwargs)
            
            if encoded: string = encode_save(string)
            
            file.write(string)
    
    
    @classmethod
    def from_plist(cls, data, load:bool=False, load_keys:Iterable=None,**kwargs):
        
        fkwargs = kwargs.setdefault('fkwargs', {})
        fkwargs.setdefault('load', load)
        fkwargs.setdefault('load_keys', load_keys)
        
        return super().from_plist(data, **kwargs)
        
    
    def to_plist(self, path:str|PathLike, save:bool=True, save_keys:Iterable=None, **kwargs):
        
        fkwargs = kwargs.setdefault('fkwargs', {})
        fkwargs.setdefault('save', save)
        fkwargs.setdefault('save_keys', save_keys)

        super().to_plist(path, **kwargs)
    

class GameSave(PlistDictDecoderMixin, DictClass):

    @classmethod
    def from_file(cls, path:str|PathLike=GAMEMANAGERPATH, encoded:bool=True, **kwargs):
                    
        with open(path, "r") as file:
            
            string = file.read()
            
            if encoded: string = decode_save(string)
            
            return super().from_string(string, **kwargs)
    
    
    @classmethod
    def to_file(self, path:str|PathLike=GAMEMANAGERPATH, encoded:bool=True, **kwargs):
                    
        with open(path, "w") as file:
            
            string = super().to_string(**kwargs)
            
            if encoded: string = encode_save(string)
            
            file.write(string)
            
            
if __name__ == "__main__":
    level_data = LevelSave.from_file()
    levels = level_data['LLM_01']
    binary = level_data['LLM_02']
    lists = level_data['LLM_03']
    
    game_data = GameSave.from_file()