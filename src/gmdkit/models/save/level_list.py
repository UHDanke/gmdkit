# Imports
from collections.abc import Iterable
from functools import partial
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
    
    DECODER = staticmethod(dict_cast({
        "LLM_01": LevelList.from_plist,
        "LLM_03": LevelPackList.from_plist    
        }))   
    ENCODER = staticmethod(dict_cast({
        "LLM_01": to_plist,
        "LLM_03": to_plist   
        }))   
    
    
    @classmethod
    def from_plist(cls, data, load:bool=False, load_keys:Iterable|None=None,**kwargs):
        
        decoder = dict_cast({
            "LLM_01": partial(LevelList.from_plist, load=load, load_keys=load_keys),
            "LLM_03": LevelPackList.from_plist    
            })
        
        return super().from_plist(data, decoder=decoder, **kwargs)
        
    
    def to_plist(self, path:str|PathLike, save:bool=True, save_keys:Iterable|None=None, **kwargs):
        
        encoder = dict_cast({
            "LLM_01": partial(to_plist, save=save, save_keys=save_keys),
            "LLM_03": to_plist   
            })
        
        super().to_plist(path, encoder=encoder, **kwargs)
    

if __name__ == "__main__":
    level_data = LevelSave.from_file()
    levels = level_data[lvl_save.LEVELS]
    binary = level_data[lvl_save.BINARY]
    lists = level_data[lvl_save.LISTS]