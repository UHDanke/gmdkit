# Package Imports
from gmdkit.utils.types import ListClass
from gmdkit.serialization.mixins import ArrayDecoderMixin, DataclassDecoderMixin
from gmdkit.serialization.functions import dataclass_decoder


class IntList(ArrayDecoderMixin,ListClass[int]):
    
    __slots__ = ()
    
    SEPARATOR = ","
    GROUP_SIZE = 1
    DECODER = int
    ENCODER = str


@dataclass_decoder(slots=True, separator="~", from_array=True)
class IntPair(DataclassDecoderMixin):
    key: int = 0
    value: int = 0
    

class IntPairList(ArrayDecoderMixin,ListClass[IntPair]):
    
    __slots__ = ()
    
    SEPARATOR = "."
    GROUP_SIZE = 2
    DECODER = IntPair.from_tokens
    ENCODER = IntPair.to_tokens
       
    def keys(self):
        return self.unique_values(lambda x: [x.key])
    
    def values(self):
        return self.unique_values(lambda x: [x.value])
    
    def remap_keys(self, dictionary:dict[int,int]):
        if dictionary:
            for pair in self:
                k = pair.key
                pair.key = dictionary.get(k, k)

    
