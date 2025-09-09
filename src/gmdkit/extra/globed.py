# Imports
import zstandard as zstd
import struct
from pathlib import Path
from os import PathLike

# Package Imports
from gmdkit.models.object import Object, ObjectList
from gmdkit.models.prop.text import EncodedString
from gmdkit.mappings import prop_id, obj_id

MAGIC = b'\xc4\x19\x7b\xfa'
PREFIX = "GLOBED_SCRIPT"



import zstandard as zstd
import struct


def check_magic(data:bytes):
        
    null_pos = data.find(b"\x00")
        
    if null_pos == -1:
        return False

    magic_pos = data.find(MAGIC)
        
    return magic_pos == null_pos + 1


def decode_script(data:bytes):
    
    if not check_magic(data):
        raise ValueError("Invalid header, magic does not match.")
    
    i = data.find(b'\x00'+MAGIC)
    
    prefix = (data[:i]).decode("utf-8",errors="surrogateescape")
    i += 1 + len(MAGIC)

    data_size = struct.unpack_from("<I", data, i)[0]
    i += 4

    decompressed = zstd.decompress(data[i:],max_output_size=data_size)
    mv = memoryview(decompressed)
    j = 0
    
    is_main = bool(mv[j])
    j += 1
    
    filename_size = struct.unpack_from("<H", mv, j)[0]
    j += 2
    filename = mv[j:j+filename_size].tobytes().decode("utf-8")
    j += filename_size
    
    content_size = struct.unpack_from("<I", mv, j)[0]
    j += 4
    content = mv[j:j+content_size].tobytes().decode("utf-8")
    j += content_size
    print(mv[j:].tobytes())
    has_signature = bool(mv[j])
    j += 1
    
    if has_signature:
        signature = mv[j:j+32].tobytes()
        j += 32
    else:
        signature = None
    
    # pass on remaining bytes as tail
    if (remaining:=mv[j:].tobytes()):
        tail = remaining
    else:
        tail = None
    
    return prefix, is_main, filename, content, signature, tail


def encode_script(
        prefix:str=None,
        filename:str=None,
        content:str=None,
        is_main:bool=False,
        signature:bytes=None,
        tail:bytes=None
        ):
    
    result = bytearray()
    
    if prefix is None: prefix = PREFIX
    prefix_bytes = prefix.encode("utf-8",errors="surrogateescape")    
    result.extend(prefix_bytes)
    result.extend(b'\x00' + MAGIC)
    
    data = bytearray()
    
    data.append(1 if is_main else 0)
    
    if filename is None: filename = ""
    filename_bytes = filename.encode("utf-8")
    filename_size = len(filename_bytes)
    if filename_size > 2**16-1: 
        raise ValueError(f"Filename is too long: {filename_size} bytes, should be {2**16-1} at most")
    
    data.extend(struct.pack("<H", filename_size))
    data.extend(filename_bytes)
    
    if content is None: content = ""
    content_bytes = content.encode("utf-8")
    content_size = len(content_bytes)
    if content_size > 2**32-1: 
        raise ValueError(f"Content is too long: {content_size} bytes, should be {2**32-1} at most")
    
    data.extend(struct.pack("<I", content_size))
    data.extend(content_bytes)
    
    if signature is not None:
        data.append(1)
        if len(signature) != 32: raise ValueError(f"Invalid signature length: {len(signature)} bytes, should be 32 exactly")
        data.extend(signature)
    
    else:
        data.append(0)

    if tail is not None:
        data.extend(tail)
    
    data_size = len(data)
    result.extend(struct.pack("<I", data_size))
    
    compressed = zstd.compress(data, level=8)
    result.extend(compressed)
    
    return result


def is_text_object(obj:Object):
    
    if not isinstance(obj, dict):
        raise ValueError(f"Object is of type <{type(obj)}>, not a dict-like object.")
    
    if (val:=obj.get(prop_id.id)) != obj_id.text:
        raise ValueError(f"Object ID {val} is not a text object {obj_id.text}")
    
    return True
        
           
class GlobedScript:
    
    __slots__ = ("bytes","object","prefix","main","filename","content","signature","tail")
    
    
    def __init__(self, obj:Object=None):
        
        self.bytes: bytes = None
        self.object: Object = obj
        self.prefix: str = None
        self.main: str = None
        self.filename: str = None
        self.content: str = None
        self.signature: bytes = None
        self.tail: bytes = None
        
        if self.object is not None:
            self.load()
        
    
    def decode(self):
        pre, main, fn, content, sig, tail = decode_script(self.bytes)
        self.prefix = pre
        self.main = main
        self.filename = fn
        self.content = content
        self.signature  = sig
        self.tail = tail
        
    def encode(self):
        data = encode_script(
            prefix=self.prefix,
            is_main=self.main,
            filename=self.filename,
            content=self.content,
            signature=self.signature,
            tail=self.tail
            )
        self.bytes = data

    def load(self):
        try:
            is_text_object(self.object)
            string = self.object.get(prop_id.text.data)
            self.bytes = string.to_bytes()
            self.decode()
    
        except Exception as e:
            raise RuntimeError(f"Error while loading script data: {e}") from e
    
    
    def save(self):
        try:
            is_text_object(self.object)
            self.encode()
            string = EncodedString().from_bytes(self.bytes)
            self.object[prop_id.text.data] = string
            
        except Exception as e:
            raise RuntimeError(f"Error while saving script data to object: {e}") from e


    def import_script(self, path:str|PathLike, include_name:bool=False):
        
        with open(path,"r") as file:
            self.content = file.read()
        
        if include_name:
            self.filename = Path(path).name
    
    
    def export_script(self, path:str|PathLike, extension:str="lua"):
        
        path = Path(path)
        
        if not path.suffix:
            path = (path / self.filename).with_suffix('.' + extension.lstrip('.'))
                    
        with open(path,"w") as file:
            file.write(self.content)


def get_globed_scripts(obj_list:ObjectList):
    
    result = []
    
    for obj in ObjectList:
        
        if obj_id.text != obj.get(prop_id.id):
            continue
        
        string = obj.get(prop_id.text.data)
        
        if string is None:
            continue
        
        if not check_magic(string.to_bytes()):
            continue
        
        try:
            result.append(GlobedScript(obj))
            
        except Exception as e:
            print("Object skipped due to unforseen error while loading GlobedScript:", e)
        
    return result


if __name__ == "__main__":
    
    example_script = """function hello_world()\n\tprint("Hello, world!")\nend\n\nhello_world()"""

    binary = encode_script(filename="hello.lua", content=example_script)
    import base64

    base_64 = base64.urlsafe_b64encode(binary).decode()

    decoded = decode_script(binary)
    
    globed = b'R0xPQkVEX1NDUklQVADEGXv6IwAAACi1L_0gIxkBAAAKAHNjcmlwdC5sdWERAAAALS0gWW91ciBjb2RlIGhlcmUA'
    
    globed_decode = decode_script(base64.urlsafe_b64decode(globed))