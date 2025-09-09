# Imports
from typing import Self
from collections.abc import Iterable
from pathlib import Path
from os import PathLike

# Package Imports
from gmdkit.models.object import Object, ObjectList
from gmdkit.models.types import ListClass, DictClass
from gmdkit.models.serialization import PlistDictDecoderMixin, PlistArrayDecoderMixin, dict_cast
from gmdkit.casting.level_props import LIST_ENCODERS, LIST_DECODERS
from gmdkit.mappings import lvl_id

class LevelPack(PlistDictDecoderMixin,DictClass):
    
    __slots__ = ()
    
    DECODER = staticmethod(dict_cast(LIST_DECODERS, numkey=True))
    ENCODER = staticmethod(dict_cast(LIST_ENCODERS, numkey=True))
        
    def to_file(self, path:str|PathLike, extension:str="gmdl", **kwargs):
        
        path = Path(path)
        
        if not path.suffix:
            path = (path / self[lvl_id.list.name]).with_suffix('.' + extension.lstrip('.'))
            
        super().to_file(path=path, **kwargs)
                

class LevelPackList(PlistArrayDecoderMixin,ListClass):
    
    __slots__ = ()
    
    DECODER = LevelPack.from_plist
    ENCODER = staticmethod(lambda x, **kwargs: x.to_plist(**kwargs))