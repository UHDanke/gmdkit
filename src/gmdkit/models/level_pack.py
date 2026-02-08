# Imports
from pathlib import Path
from os import PathLike

# Package Imports
from gmdkit.serialization.types import ListClass, DictClass
from gmdkit.serialization.mixins import PlistDictDecoderMixin, PlistArrayDecoderMixin
from gmdkit.serialization.type_cast import dict_cast, to_plist
from gmdkit.casting.list_props import LIST_ENCODERS, LIST_DECODERS
from gmdkit.mappings import list_prop

class LevelPack(PlistDictDecoderMixin,DictClass):
    
    __slots__ = ()
    
    DECODER = staticmethod(dict_cast(LIST_DECODERS, numkey=True))
    ENCODER = staticmethod(dict_cast(LIST_ENCODERS, numkey=True))
    
    def to_file(self, 
            path:str|PathLike|None=None, 
            extension:str="gmdl", 
            **kwargs):
        
        if path is None: 
            path = Path()
        else:
            path = Path(path)
        
        if not path.suffix:
            path = (path / self[list_prop.NAME]).with_suffix('.' + extension.lstrip('.'))
            
        super().to_file(path=path, **kwargs)

        
class LevelPackList(PlistArrayDecoderMixin,ListClass):
    
    __slots__ = ()
    
    DECODER = LevelPack.from_plist
    ENCODER = staticmethod(to_plist)