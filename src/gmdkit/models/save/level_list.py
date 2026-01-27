# Imports
from collections.abc import Iterable
from typing import Self
from os import PathLike

# Package Imports
from gmdkit.models.level import LevelList
from gmdkit.models.level_pack import LevelPackList
from gmdkit.serialization.types import DictClass
from gmdkit.serialization.type_cast import dict_cast, to_plist
from gmdkit.serialization.mixins import PlistDictDecoderMixin, LoadFileMixin
from gmdkit.constants.paths.save import LOCAL_LEVELS_PATH
from gmdkit.mappings import lvl_save

class LevelSave(LoadFileMixin,PlistDictDecoderMixin,DictClass):
    
    DEFAULT_PATH = LOCAL_LEVELS_PATH
    COMPRESSION = "gzip"
    CYPHER = bytes([11])
    
    DECODER = staticmethod(dict_cast({"LLM_01": LevelList.from_plist,"LLM_03": LevelPackList.from_plist}))   
    ENCODER = staticmethod(to_plist)    
    
    @classmethod
    def from_plist(cls, data, load:bool=False, load_keys:Iterable|None=None,**kwargs) -> Self:
        
        fkwargs = kwargs.setdefault('fkwargs', {})
        fkwargs.setdefault('load', load)
        fkwargs.setdefault('load_keys', load_keys)
        
        return super().from_plist(data, **kwargs)
        
    
    def to_plist(self, path:str|PathLike, save:bool=True, save_keys:Iterable|None=None, **kwargs):
        
        fkwargs = kwargs.setdefault('fkwargs', {})
        fkwargs.setdefault('save', save)
        fkwargs.setdefault('save_keys', save_keys)

        super().to_plist(path, **kwargs)
    

if __name__ == "__main__":
    level_data = LevelSave.from_file()
    levels = level_data[lvl_save.LEVELS]
    binary = level_data[lvl_save.BINARY]
    lists = level_data[lvl_save.LISTS]