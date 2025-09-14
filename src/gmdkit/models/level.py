# Imports
from typing import Self
from collections.abc import Iterable
from pathlib import Path
from os import PathLike

# Package Imports
from gmdkit.models.object import Object, ObjectList
from gmdkit.models.types import ListClass, DictClass
from gmdkit.models.serialization import decode_string, PlistDictDecoderMixin, PlistArrayDecoderMixin, dict_cast
from gmdkit.models.prop.string import GzipString
from gmdkit.models.prop.gzip import ObjectString, ReplayString
from gmdkit.casting.level_props import LEVEL_ENCODERS, LEVEL_DECODERS
from gmdkit.mappings import lvl_id


LEVEL_DEFAULT = {
    'kCEK': 4,
    'k4': 'H4sIAAAAAAAACqWT0W3EMAxDF3IBUZITB_26GW4ADnAr3PCNzAD9SZEU9yPGIfUiGcjrGaOBaXTCO4PeOwGJS_Qy-QUuhJlxJYheZdA4iDc4Eeb3EPgcsZ0iKqOGWxBn9Z-B_nUl-_lzRp4ysPnvQp5XC_U_F9LNYBTIrjDLBeb2BZ8t1V4PRLOSLlkk2faq53VWP3ydMEqescmbVZxpPHJWuTCFlHLFXAlfGypuEkh8igvlooS8kBcaLQVLwbKrXV6EkinR-KHv1Z9Wsk3BsYX6_BgXGn6X7x_T2S7pmwMAAA==',
    'k13': True,
    'k21': 2,
    'k16': 1,
    'k50': 45,
    'k47': True
    }


class Level(PlistDictDecoderMixin,DictClass):
    
    DECODER = staticmethod(dict_cast(LEVEL_DECODERS))
    ENCODER = staticmethod(dict_cast(LEVEL_ENCODERS))
    
    
    def __init__(self, *args, load:bool=False, load_keys:Iterable=None,**kwargs):
        
        super().__init__(*args, **kwargs)
        
        if load: self.load(keys=load_keys)


    @classmethod
    def from_file(cls, path:str|PathLike, load:bool=True, load_keys:Iterable=None, **kwargs):
                
        return super().from_file(path, load=load, load_keys=load_keys, **kwargs)
    
    
    def to_file(self, path:str|PathLike, extension:str="gmd", save:bool=True, save_keys:Iterable=None, **kwargs):
        
        path = Path(path)
        
        if not path.suffix:
            path = (path / self[lvl_id.level.name]).with_suffix('.' + extension.lstrip('.'))
            
        super().to_file(path=path, save=save, save_keys=save_keys, **kwargs)

    
    def to_plist(self, save:bool=True, save_keys:Iterable=None, **kwargs):
        
        if save: self.save(keys=save_keys)
        
        super().to_plist(**kwargs)

    
    @property
    def object_string(self):
        
        return decode_string(self.get(lvl_id.level.object_string))
        
        
    def load(self, keys:Iterable=None):
        
        keys = keys or self.keys()
        
        for key in keys:
            
            value = self.get(key)
            
            if issubclass(type(value), GzipString):
                value.decompress(instance=self)            
    
            
    def save(self, keys:Iterable=None):
        
        keys = keys or self.keys()
        
        seen = set()
        
        for key in keys:
            
            seen.add(key)
            
            value = self.get(key)
                        
            if issubclass(type(value), GzipString):
                self[key] = value.compress(instance=self)
    
    @classmethod
    def default(cls, name:str,load:bool=True):
        
        data = LEVEL_DEFAULT.copy()        
        data[lvl_id.level.name] = name
        
        kwargs = {}
        kwargs["load"] = load
        
        return cls.from_plist(data, **kwargs)


class LevelList(PlistArrayDecoderMixin,ListClass):
    
    __slots__ = ()
    
    DECODER = Level.from_plist
    ENCODER = staticmethod(lambda x, **kwargs: x.to_plist(**kwargs))
    
    
    def __init__(self, *args):
        
        super().__init__(*args)      
    
        
    @classmethod
    def from_plist(cls, data, load_levels:bool=False, load_keys:Iterable=None,**kwargs):
        
        fkwargs = kwargs.setdefault('fkwargs', {})
        fkwargs.setdefault('load', load_levels)
        fkwargs.setdefault('load_keys', load_keys)
        
        return super().from_plist(data, **kwargs)
        
    
    def to_plist(self, path:str|PathLike, save_levels:bool=True, save_keys:Iterable=None, **kwargs):
        
        fkwargs = kwargs.setdefault('fkwargs', {})
        fkwargs.setdefault('save', save_levels)
        fkwargs.setdefault('save_keys', save_keys)

        super().to_plist(path, **kwargs)