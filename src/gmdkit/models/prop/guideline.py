# Imports
from json import loads as dict_from_string, dumps as dict_to_string

# Package Imports
from gmdkit.utils.types import ListClass
from gmdkit.serialization.mixins import ArrayDecoderMixin, DataclassDecoderMixin,DelimiterMixin,FileStringMixin
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.serialization.type_cast import decode_text, encode_text


# Some mods use guideline data as a datafield
# this exists in order to allow gmdkit to load the level
@dataclass_decoder(slots=True, separator="~", from_array=True)
class Guidedata(DataclassDecoderMixin):

    data: dict = field_decoder(
        decoder=lambda string: dict_from_string(decode_text(string.removeprefix("|"))), 
        encoder=lambda value: "|" + encode_text(dict_to_string(value))
        )
    unk: float = 0


@dataclass_decoder(slots=True, separator="~", from_array=True)
class Guideline(DataclassDecoderMixin):

    time: float = 0
    color: float = 0


class GuidelineList(FileStringMixin,DelimiterMixin,ArrayDecoderMixin,ListClass[Guideline|Guidedata]):
    
    __slots__ = ()
    
    SEPARATOR = "~"
    END_DELIMITER = "~"
    GROUP_SIZE = 2
    DECODER = lambda t: Guidedata.from_tokens(t) if t[0].startswith("|") else Guideline.from_tokens(t)
    ENCODER = lambda obj: obj.to_tokens()
    
    def clean(self):
        
        new = []
        
        for p in self:
            
            if p.value in [0,0.9,1.0]: pass
            elif p.value > 0.8: p.value = 0
            else: continue

            new.append(p)
        
        self[:] = new