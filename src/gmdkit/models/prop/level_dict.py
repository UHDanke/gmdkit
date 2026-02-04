from gmdkit.serialization.types import DictClass
from gmdkit.serialization.mixins import PlistDictDecoderMixin
from gmdkit.serialization.type_cast import to_plist
from gmdkit.models.level import Level


def dict_to_level(key:int|str, dictionary:dict, **kwargs):
    return (key, Level(dictionary, **kwargs))


def level_to_dict(key:int|str, value:Level, **kwargs):
    return (key, to_plist(value))


class LevelMapping(PlistDictDecoderMixin,DictClass):
    DECODER = staticmethod(dict_to_level)   
    ENCODER = staticmethod(level_to_dict)  
    