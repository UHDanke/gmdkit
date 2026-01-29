# Package Imports
from gmdkit.models.level import Level, LevelList
from gmdkit.serialization.type_cast import dict_cast, to_plist
from gmdkit.casting.list_props import LIST_ENCODERS, LIST_DECODERS


class LevelPack(Level):
    
    __slots__ = ()
    
    DECODER = staticmethod(dict_cast(LIST_DECODERS, numkey=True))
    ENCODER = staticmethod(dict_cast(LIST_ENCODERS, numkey=True))
                

class LevelPackList(LevelList):
    
    __slots__ = ()
    
    DECODER = LevelPack.from_plist
    ENCODER = staticmethod(to_plist)