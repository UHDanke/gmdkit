# Imports
import base64
from typing import Self

# Package Imports
from gmdkit.models.serialization import decode_string, encode_string
 

def decode_text(string:str) -> str:
    
    string_bytes = string.encode("utf-8")
    
    decoded_bytes = base64.urlsafe_b64decode(string_bytes)
    
    return decoded_bytes.decode("utf-8", errors="surrogateescape")


def encode_text(string:str) -> str:
    
    string_bytes = string.encode("utf-8", errors="surrogateescape")
    
    encoded_bytes = base64.urlsafe_b64encode(string_bytes)
    
    return encoded_bytes.decode("utf-8")

 
class GzipString:
    
    __slots__ = ("string")
    
    
    def __init__(self, string:str=""):
        self.string = string
    
    def load(self) -> str:
        return decode_string(self.string)
        
    def save(self, string) -> None:
        new = encode_string(string)
        self.string = new
        return self.string