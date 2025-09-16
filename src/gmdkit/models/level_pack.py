# Package Imports
from gmdkit.models.object import Object, ObjectList
from gmdkit.models.level import Level, LevelList
from gmdkit.models.serialization import dict_cast
from gmdkit.casting.level_props import LIST_ENCODERS, LIST_DECODERS


class LevelPack(Level):
    
    __slots__ = ()
    
    DECODER = staticmethod(dict_cast(LIST_DECODERS, numkey=True))
    ENCODER = staticmethod(dict_cast(LIST_ENCODERS, numkey=True))
                

class LevelPackList(LevelList):
    
    __slots__ = ()
    
    DECODER = LevelPack.from_plist
    ENCODER = staticmethod(lambda x, **kwargs: x.to_plist(**kwargs))