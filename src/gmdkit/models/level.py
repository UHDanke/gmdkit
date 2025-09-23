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
from gmdkit.defaults.level import LEVEL_DEFAULT
from gmdkit.mappings import lvl_prop


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
            path = (path / self[lvl_prop.level.NAME]).with_suffix('.' + extension.lstrip('.'))
            
        super().to_file(path=path, save=save, save_keys=save_keys, **kwargs)

    
    def to_plist(self, save:bool=True, save_keys:Iterable=None, **kwargs):
        
        if save: self.save(keys=save_keys)
        
        return super().to_plist(**kwargs)

        
    def load(self, keys:Iterable=None, copy_attributes:bool=True):
        
        keys = keys or self.keys()
        
        for key in keys:
            
            value = self.get(key)
            
            if issubclass(type(value), GzipString):
                value.load()
                
                if not copy_attributes: continue
                
                for attr, value in vars(value).items():
                    
                    if attr.startswith("_"): continue
                    if attr == "string": continue
                    
                    setattr(self, attr, value)
    
            
    def save(self, keys:Iterable=None):
        
        keys = keys or self.keys()
        
        seen = set()
        
        for key in keys:
            
            seen.add(key)
            
            value = self.get(key)
                        
            if issubclass(type(value), GzipString):
                value.save()
        
    
    @classmethod
    def default(cls, name:str,load:bool=True):
        
        data = LEVEL_DEFAULT.copy()        
        data[lvl_prop.level.NAME] = name
        
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
    def from_plist(cls, data, load:bool=False, load_keys:Iterable=None,**kwargs):
        
        fkwargs = kwargs.setdefault('fkwargs', {})
        fkwargs.setdefault('load', load)
        fkwargs.setdefault('load_keys', load_keys)
        
        return super().from_plist(data, **kwargs)
        
    
    def to_plist(self, path:str|PathLike, save:bool=True, save_keys:Iterable=None, **kwargs):
        
        fkwargs = kwargs.setdefault('fkwargs', {})
        fkwargs.setdefault('save', save)
        fkwargs.setdefault('save_keys', save_keys)

        super().to_plist(path, **kwargs)