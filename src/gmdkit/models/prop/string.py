# Imports
import base64
from typing import Self

# Package Imports
from gmdkit.models.types import StrClass
from gmdkit.models.serialization import decode_string, encode_string


class TextString(StrClass):
    
    __slots__ = ()
    
    
    @classmethod
    def decode_string(cls, string:str) -> Self:
        data = base64.urlsafe_b64decode(string.encode("utf-8"))
        return cls.from_bytes(data)

    
    def encode_string(self) -> str:
        binary = base64.urlsafe_b64encode(self.to_bytes())
        return binary.decode()
    
    
    @classmethod
    def from_bytes(cls, data:bytes) -> Self:

        return cls(data.decode("utf-8",errors='surrogateescape'))
    
    
    def to_bytes(self) -> bytes:
        return self.encode("utf-8", errors="surrogateescape")
    
    
class GzipString(StrClass):
    
    __slots__ = ()
    
    def decompress(self) -> str:
        
        return decode_string(self)
        
    def compress(self, string) -> None:
        
        new = encode_string(string)
        
        self[:] = new

        return new