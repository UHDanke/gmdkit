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

class LevelSave(PlistDictDecoderMixin, DictClass):
    
    DECODER = staticmethod(dict_cast({"LLM_01": LevelList.from_plist,"LLM_03": LevelPackList.from_plist}, key_kwargs=True))   
    ENCODER = staticmethod(lambda x, **kwargs: x.to_plist(**kwargs))
    
    @classmethod
    def from_file(cls, path:str|PathLike=None, **kwargs):
        
        if path is None:
            path = LOCALPATH / "CCLocalLevels.dat"
            
        with open(path, "r") as file:
            string = decode_save(file.read())
            return super().from_string(string, **kwargs)
    
    
    @classmethod
    def to_file(self, path:str|PathLike=None, **kwargs):
        
        if path is None:
            path = LOCALPATH / "CCLocalLevels.dat"
            
        with open(path, "w") as file:
            string = encode_save(super().to_string(**kwargs))
            file.write(string)
    
    
    @classmethod
    def from_plist(cls, data, load_levels:bool=False, load_keys:Iterable=None,**kwargs):
        
        fkwargs = kwargs.setdefault('fkwargs', {})
        lvl_kwargs = fkwargs.setdefault('LLM_01',{})
        lvl_kwargs.setdefault('load_levels', load_levels)
        lvl_kwargs.setdefault('load_keys', load_keys)
        
        return super().from_plist(data, **kwargs)
        
    
    def to_plist(self, path:str|PathLike, save_levels:bool=True, save_keys:Iterable=None, **kwargs):
        
        fkwargs = kwargs.setdefault('fkwargs', {})
        lvl_kwargs = fkwargs.setdefault('LLM_01',{})
        lvl_kwargs.setdefault('save_levels', save_levels)
        lvl_kwargs.setdefault('save_keys', save_keys)

        super().to_plist(path, **kwargs)
    
            
            
if __name__ == "__main__":
    level_data = LevelSave.from_file()
    levels = level_data['LLM_01']
    binary = level_data['LLM_02']
    lists = level_data['LLM_03']
    