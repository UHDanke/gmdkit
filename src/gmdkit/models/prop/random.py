# Package Imports
from gmdkit.models.prop.list import IntPair, IntPairList


class RandomWeightsList(IntPairList):
    
    __slots__ = ()
    
    @classmethod
    def from_dict(cls, data:dict[int,int]):
        
        result = cls()
        
        for key, value in data.items():
            result.append(IntPair(key,value))
        
        return result
    
    
    def to_dict(self) -> dict[int,int]:
        
        result = {}
        
        for p in self:
            result[p.key] = result.get(p.key,0) + p.value
        
        return result