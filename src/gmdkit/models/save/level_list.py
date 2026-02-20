# Imports
from typing import Self, TYPE_CHECKING

# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.utils.typing import PathString
from gmdkit.models.level import LevelList
from gmdkit.models.level_pack import LevelPackList
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


class LevelSave(CompressFileMixin,PlistDictDecoderMixin,DictClass):
    
    DEFAULT_PATH = LOCAL_LEVELS_PATH
    COMPRESSION = "gzip"
    CYPHER = bytes([11])
    
    DECODER = staticmethod(dict_cast(LEVEL_SAVE_DECODER, allowed_kwargs={"LLM_01":{"load"}}))   
    ENCODER = staticmethod(dict_cast(LEVEL_SAVE_ENCODER, allowed_kwargs={"LLM_01":{"save"}})) 
    
    @classmethod
    def from_plist(cls, data, load:bool=False, **kwargs) -> Self:
        return super().from_plist(data, load=load, **kwargs)

    def to_plist(self, save:bool=True, **kwargs) -> list:
        return super().to_plist(save=save, **kwargs)
    
    if TYPE_CHECKING:
        @classmethod
        def from_file(cls, path:PathString, load:bool=False, **kwargs) -> Self: ...
        
        def to_file(self, path:PathString, save:bool=False, **kwargs): ...


if __name__ == "__main__":
    level_data = LevelSave.from_file()
    levels = level_data[lvl_save.LEVELS]
    binary = level_data[lvl_save.BINARY]
    lists = level_data[lvl_save.LISTS]