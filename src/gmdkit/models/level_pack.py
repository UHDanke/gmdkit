# Imports
from collections.abc import Iterable
from os import PathLike

# Package Imports
from gmdkit.models.level import Level, LevelList
from gmdkit.serialization.type_cast import dict_cast, to_plist
from gmdkit.casting.list_props import LIST_ENCODERS, LIST_DECODERS


class LevelPack(Level):
    
    __slots__ = ()
    
    DECODER = staticmethod(dict_cast(LIST_DECODERS, numkey=True))
    ENCODER = staticmethod(dict_cast(LIST_ENCODERS, numkey=True))
    
    def to_file(self, 
            path:str|PathLike|None=None, 
            extension:str="gmdl", 
            save:bool=True, 
            save_keys:Iterable|None=None, 
            **kwargs):
        
        return super().to_file(
                path=path,
                extension=extension,
                save=save,
                save_keys=save_keys
            )

class LevelPackList(LevelList):
    
    __slots__ = ()
    
    DECODER = LevelPack.from_plist
    ENCODER = staticmethod(to_plist)