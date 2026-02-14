# Package Imports
from gmdkit.models.level import LevelList
from gmdkit.models.level_pack import LevelPackList
from gmdkit.serialization.types import DictClass
from gmdkit.serialization.type_cast import dict_cast, to_plist
from gmdkit.serialization.mixins import PlistDictDecoderMixin, CompressFileMixin
from gmdkit.constants.paths.save import LOCAL_LEVELS_PATH
from gmdkit.mappings import lvl_save


LEVEL_SAVE_DECODER = {
    "LLM_01": LevelList.from_plist,
    "LLM_03": LevelPackList.from_plist    
    }

LEVEL_SAVE_ENCODER = {
    "LLM_01": to_plist,
    "LLM_03": to_plist   
    }

def kwargs_load(load:bool=False, **kwargs):
    return {"load":load}

def kwargs_save(save:bool=True, **kwargs):
    return {"save":save}

class LevelSave(CompressFileMixin,PlistDictDecoderMixin,DictClass):
    
    DEFAULT_PATH = LOCAL_LEVELS_PATH
    COMPRESSION = "gzip"
    CYPHER = bytes([11])
    
    DECODER = staticmethod(dict_cast(LEVEL_SAVE_DECODER, key_kwargs={"LLM_01":kwargs_load}))   
    ENCODER = staticmethod(dict_cast(LEVEL_SAVE_ENCODER, key_kwargs={"LLM_01":kwargs_save}))
    

if __name__ == "__main__":
    level_data = LevelSave.from_file()
    levels = level_data[lvl_save.LEVELS]
    binary = level_data[lvl_save.BINARY]
    lists = level_data[lvl_save.LISTS]