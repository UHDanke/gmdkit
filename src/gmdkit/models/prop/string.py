# Imports
import base64

# Package Imports
from gmdkit.serialization.functions import decode_string, encode_string
 

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
    ENCODED = True
    
    def __init__(self, string:str=""):
        self.string = string
    
    def load(self) -> str:
        if self.ENCODED:
            return decode_string(self.string)
        else:
            return self.string
        
    def save(self, string:str) -> None:
        if self.ENCODED:
            string = encode_string(string)
        self.string = string
        return self.string