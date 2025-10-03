# Imports
from collections.abc import Iterable
from typing import Self
from os import PathLike

# Package Imports
from gmdkit.models.level import Level, LevelList
from gmdkit.models.level_pack import LevelPack, LevelPackList
from gmdkit.models.types import DictClass
from gmdkit.models.serialization import PlistDictDecoderMixin, LoadFileMixin, dict_cast
from gmdkit.constants.paths import LOCAL_LEVELS_PATH


class LevelSave(LoadFileMixin,PlistDictDecoderMixin,DictClass):
    
    DEFAULT_PATH = LOCAL_LEVELS_PATH
    COMPRESSION = "gzip"
    CYPHER = bytes([11])
    
    DECODER = staticmethod(dict_cast({"LLM_01": LevelList.from_plist,"LLM_03": LevelPackList.from_plist}))   
    ENCODER = staticmethod(lambda x, **kwargs: x.to_plist(**kwargs))    
    
    @classmethod
    def from_plist(cls, data, load:bool=False, load_keys:Iterable=None,**kwargs) -> Self:
        
        fkwargs = kwargs.setdefault('fkwargs', {})
        fkwargs.setdefault('load', load)
        fkwargs.setdefault('load_keys', load_keys)
        
        return super().from_plist(data, **kwargs)
        
    
    def to_plist(self, path:str|PathLike, save:bool=True, save_keys:Iterable=None, **kwargs):
        
        fkwargs = kwargs.setdefault('fkwargs', {})
        fkwargs.setdefault('save', save)
        fkwargs.setdefault('save_keys', save_keys)

        super().to_plist(path, **kwargs)
    

if __name__ == "__main__":
    level_data = LevelSave.from_file()
    levels = level_data['LLM_01']
    binary = level_data['LLM_02']
    lists = level_data['LLM_03']