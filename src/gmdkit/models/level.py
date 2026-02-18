# Imports
from typing import Self, Optional, TYPE_CHECKING
from pathlib import Path
from glob import glob

# Package Imports
from gmdkit.models.object import Object, ObjectList
from gmdkit.serialization.types import ListClass, DictClass
from gmdkit.serialization.mixins import PlistDictDecoderMixin, PlistArrayDecoderMixin
from gmdkit.serialization.type_cast import dict_cast, to_plist
from gmdkit.serialization.typing import PathString
from gmdkit.casting.level_props import LEVEL_ENCODERS, LEVEL_DECODERS, LEVEL_TYPES
from gmdkit.defaults.level import LEVEL_DEFAULT
from gmdkit.mappings import lvl_prop


LOAD_KEYS = {k for k, v in LEVEL_TYPES.items() if hasattr(v, "load") and hasattr(v, "save")}


class Level(PlistDictDecoderMixin,DictClass):
    
    DECODER = staticmethod(dict_cast(LEVEL_DECODERS))
    ENCODER = staticmethod(dict_cast(LEVEL_ENCODERS))
    
    if TYPE_CHECKING:
        @classmethod
        def from_file(cls, path:PathString, load:bool=True, **kwargs) -> Self: ...
    
    def to_file(self, 
            path:Optional[PathString]=None, 
            extension:str="gmd", 
            save:bool=True,
            **kwargs):
        
        if path is None: 
            path = Path()
        else:
            path = Path(path)
        
        if not path.suffix:
            path = (path / self[lvl_prop.NAME]).with_suffix('.' + extension.lstrip('.'))
            
        super().to_file(path=path, save=save, **kwargs)
        
        
    @classmethod
    def from_plist(cls, data:dict, load:bool=True, **kwargs) -> Self:
        
        new = super().from_plist(data, **kwargs)
        
        if load: new.load()
        
        return new
    

    def to_plist(self, save:bool=True, **kwargs) -> dict:
        
        if save: self.save()
        
        return super().to_plist(**kwargs)

        
    def load(self):
        for key in self.keys() & LOAD_KEYS:
            value = self.get(key)
            load = getattr(value, "load", None)
    
            if load is not None and callable(load):
                load()
        
            
    def save(self):    
        for key in self.keys() & LOAD_KEYS:
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
    
    # TODO REDO
    @classmethod
    def default(cls, name:str,load:bool=True):
        
        data = LEVEL_DEFAULT.copy()        
        data[lvl_prop.NAME] = name
                
        return cls.from_plist(data, load=load)


class LevelList(PlistArrayDecoderMixin,ListClass):
    
    __slots__ = ()
    
    DECODER = Level.from_plist
    ENCODER = staticmethod(to_plist)
    
    
    @classmethod
    def from_folder(cls, path:PathString, extension:str='.gmd', load:bool=False):
        
        new = cls()
        
        folder_path = str(Path(path) / ('*' + extension))
        
        for file in glob(folder_path):
            level = Level.from_file(file, load=load)
            
            new.append(level)
        
        return new
    
    
    def to_folder(self, path:PathString):
        
        folder_path = Path(path)
        
        if not folder_path.is_dir():
            raise ValueError("Given path is not a directory.")
        
        for lvl in self:
            lvl.to_file(folder_path)
    
    
    if TYPE_CHECKING:
        @classmethod
        def from_file(cls, path:PathString, load:bool=False, **kwargs) -> Self: ...
        
        def to_file(self, path:PathString, save:bool=False, **kwargs): ...
        
        @classmethod
        def from_plist(cls, data, load:bool=False, **kwargs) -> Self: ...
    
        def to_plist(self, save:bool=True, **kwargs) -> list: ...

        

        
    