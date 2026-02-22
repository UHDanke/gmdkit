# Package Imports
from gmdkit.utils.types import ListClass
from gmdkit.serialization.mixins import ArrayDecoderMixin, DataclassDecoderMixin,DelimiterMixin
from gmdkit.serialization.functions import dataclass_decoder


@dataclass_decoder(slots=True, separator="~", from_array=True)
class Guideline(DataclassDecoderMixin):

    time: float = 0
    color: float = 0


class GuidelineList(DelimiterMixin,ArrayDecoderMixin,ListClass):
    
    __slots__ = ()
    
    SEPARATOR = "~"
    END_DELIMITER = "~"
    GROUP_SIZE = 2
    DECODER = staticmethod(Guideline.from_tokens)
    ENCODER = staticmethod(Guideline.to_tokens)
    
    def clean(self):
        
        new = []
        
        for p in self:
            
            if p.value in [0,0.9,1.0]: pass
            elif p.value > 0.8: p.value = 0
            else: continue

            new.append(p)
        
        self[:] = new