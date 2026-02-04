from gmdkit.serialization.types import DictClass
from gmdkit.serialization.mixins import PlistDictDecoderMixin
from gmdkit.serialization.type_cast import to_plist
from gmdkit.models.level import Level


def dict_to_level(key, dictionary:dict, **kwargs):
    return (key, Level(dictionary, **kwargs))
    
class LevelMapping(PlistDictDecoderMixin,DictClass):
    DECODER = staticmethod(dict_to_level)   
    ENCODER = staticmethod(to_plist)  
    