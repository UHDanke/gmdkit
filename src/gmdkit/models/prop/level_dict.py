# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.utils.typing import Element
from gmdkit.serialization.mixins import PlistDecoderMixin
from gmdkit.models.level import Level


def dict_to_level(key:str, node:Element, load_level_data:bool=True, **kwargs) -> Level:
    return (int(key), Level.from_node(node=node,load_data=load_level_data,load_content=False))

def level_to_dict(key:int, level:Level, save_level_data:bool=True, **kwargs) -> Element:
    return (str(key), level.to_node(save_data=save_level_data,save_content=False))


class LevelMapping(PlistDecoderMixin,DictClass):
    DECODER = staticmethod(dict_to_level)   
    ENCODER = staticmethod(level_to_dict)  
    