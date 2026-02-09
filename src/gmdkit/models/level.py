# Imports
from collections.abc import Iterable
from functools import partial
from typing import Any
from pathlib import Path
from os import PathLike

# Package Imports
from gmdkit.models.object import Object, ObjectList
from gmdkit.serialization.types import ListClass, DictClass
from gmdkit.serialization.mixins import PlistDictDecoderMixin, PlistArrayDecoderMixin
from gmdkit.serialization.type_cast import dict_cast, to_plist
from gmdkit.casting.level_props import LEVEL_ENCODERS, LEVEL_DECODERS
from gmdkit.defaults.level import LEVEL_DEFAULT
from gmdkit.mappings import lvl_prop


class Level(PlistDictDecoderMixin,DictClass):
    
    DECODER = staticmethod(dict_cast(LEVEL_DECODERS))
    ENCODER = staticmethod(dict_cast(LEVEL_ENCODERS))
    

    @classmethod
    def from_file(cls, path:str|PathLike, **kwargs):
        
        return super().from_file(path, **kwargs)
    
    
    def to_file(self, 
            path:str|PathLike|None=None, 
            extension:str="gmd", 
            save:bool=True, 
            save_keys:Iterable|None=None, 
            **kwargs):
        
        if path is None: 
            path = Path()
        else:
            path = Path(path)
        
        if not path.suffix:
            path = (path / self[lvl_prop.NAME]).with_suffix('.' + extension.lstrip('.'))
            
        super().to_file(path=path, save=save, save_keys=save_keys, **kwargs)
        
        
    @classmethod
    def from_plist(cls, data:Any, load:bool=True, load_keys:Iterable|None=None, **kwargs):
        
        new = super().from_plist(data, **kwargs)
        
        if load: new.load(keys=load_keys)
        
        return new
    

    def to_plist(self, save:bool=True, save_keys:Iterable|None=None, **kwargs):
        
        if save: self.save(keys=save_keys)
        
        return super().to_plist(**kwargs)

        
    def load(self, keys:Iterable|None=None):
        keys = list(keys or self.keys())
    
        for key in keys:
            value = self.get(key)
            load = getattr(value, "load", None)
    
            if load is not None and callable(load):
                load()
        
            
    def save(self, keys:Iterable|None=None):
        keys = list(keys or self.keys())
    
        for key in keys:
            value = self.get(key)
            save = getattr(value, "save", None)
    
            if save is not None and callable(save):
                save()
        
    @property
    def start(self) -> Object:
        objstr = self.get(lvl_prop.OBJECT_STRING)
        
        if objstr is None:
            raise RuntimeError("Object string is missing.")
        
        if not hasattr(objstr, "start"):
            raise RuntimeError("Object string is not loaded.")

        return getattr(objstr, "start")
    
    
    @property
    def objects(self) -> ObjectList:
        objstr = self.get(lvl_prop.OBJECT_STRING)
        
        if objstr is None:
            raise RuntimeError("Object string is missing.")
        
        if not hasattr(objstr, "objects"):
            raise RuntimeError("Object string is not loaded.")

        return getattr(objstr, "objects")
    
    
    @classmethod
    def default(cls, name:str,load:bool=True):
        
        data = LEVEL_DEFAULT.copy()        
        data[lvl_prop.NAME] = name
        
        kwargs = {}
        kwargs["load"] = load
        
        return cls.from_plist(data, **kwargs)


class LevelList(PlistArrayDecoderMixin,ListClass):
    
    __slots__ = ()
    
    DECODER = Level.from_plist
    ENCODER = staticmethod(to_plist)


    @classmethod
    def from_plist(cls, data, load:bool=False, load_keys:Iterable|None=None,**kwargs):
        
        decoder = partial(cls.DECODER, load=load, load_keys=load_keys)
        
        return super().from_plist(data, decoder=decoder, **kwargs)
        
    
    def to_plist(self, path:str|PathLike, save:bool=True, save_keys:Iterable|None=None, **kwargs):
        
        encoder = partial(self.ENCODER, save=save, save_keys=save_keys)

        super().to_plist(path, encoder=encoder, **kwargs)