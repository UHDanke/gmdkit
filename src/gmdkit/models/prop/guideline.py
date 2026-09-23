# Imports
from typing import Any
from json import loads as dict_from_string, dumps as dict_to_string

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.serialization.mixins import ArrayDecoderMixin, DataclassDecoderMixin,DelimiterMixin
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.serialization.type_cast import decode_text, encode_text

# Some mods use guideline data as a datafield
# this exists in order to allow gmdkit to load the level
class Guidedata(DelimiterMixin,DictClass):
    
    @classmethod
    def from_string(cls, string:str):
        d = dict_from_string(decode_text(string.removeprefix("|")))
        return cls(**d)
    
    def to_string(self):
        return "|" + encode_text(dict_to_string(self))
    
    @classmethod
    def validate(cls, string:str):
        return string.startswith("|")  


@dataclass_decoder(slots=True, separator="~", from_array=True)
class Guideline(DataclassDecoderMixin):

    info: Any = field_decoder(
        decoder=lambda t: Guidedata.from_string(t) if Guidedata.validate(t) else float(t),
        encoder=lambda t: t.to_string() if type(t) is Guidedata else str(t),
        default=0
        )
    color: float = 0
    
    def has_metadata(self):
        return type(self.info) is not float
    
    @property
    def metadata(self) -> dict:
        return self.info if self.has_metadata() else None

    @metadata.setter
    def metadata(self, value: dict):
        self.info = value

    @property
    def time(self) -> float:
        return None if type(self.info) is float or int else self.info

    @time.setter
    def time(self, value: float):
        self.info = value


class GuidelineList(DelimiterMixin,ArrayDecoderMixin,ListClass[Guideline]):
    
    __slots__ = ()
    
    SEPARATOR = "~"
    END_DELIMITER = "~"
    GROUP_SIZE = 2
    DECODER = Guideline.from_tokens
    ENCODER = Guideline.to_tokens
    
    def clean(self):
        new = []
        last_metadata = None
    
        for g in self:
            if g.color in (0, 0.9, 1.0):
                pass
            elif g.color > 0.8:
                g.color = 0
            else:
                continue
    
            if g.has_metadata:
                last_metadata = g
            else:
                new.append(g)
    
        if last_metadata is not None:
            new.append(last_metadata)
    
        self[:] = new

        return self
    
    def get_data(self):
        d = {}
        
        for g in self:
            if g.has_metadata():
                d |= g.metadata
                
        return d if d else None