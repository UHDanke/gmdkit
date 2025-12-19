# Imports
from dataclasses import dataclass
from typing import get_type_hints

# Package Imports
from gmdkit.models.types import ListClass
from gmdkit.models.serialization import ArrayDecoderMixin, DataclassDecoderMixin, DelimiterMixin, dict_cast

    
@dataclass(slots=True)
class Guideline(DataclassDecoderMixin):
    
    SEPARATOR = "~"
    END_DELIMITER = "~"
    LIST_FORMAT = True
    
    time: float = 0
    color: float = 0
    
Guideline.DECODER = dict_cast(get_type_hints(Guideline))


class GuidelineList(DelimiterMixin,ArrayDecoderMixin,ListClass):
    
    __slots__ = ()
    
    SEPARATOR = "~"
    END_DELIMITER = "~"
    GROUP_SIZE = 2
    DECODER = staticmethod(lambda array: Guideline.from_args(*array))
    ENCODER = staticmethod(lambda pair, s=SEPARATOR: pair.to_string(separator=s))
    
    def clean(self):
        
        new = []
        
        for p in self:
            
            if p.value in [0,0.9,1.0]: pass
            elif p.value > 0.8: p.value = 0
            else: continue

            new.append(p)
        
        self[:] = new