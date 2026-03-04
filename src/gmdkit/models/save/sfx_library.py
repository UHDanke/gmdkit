# Imports
from typing import Sequence, Self

# Package Imports
from gmdkit.serialization.mixins import (
    ArrayDecoderMixin, DataclassDecoderMixin,
    DelimiterMixin, 
    CompressFileMixin,
    FilePathMixin,
    FileStringMixin,
    DefaultPathMixin
    )
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.utils.types import ListClass
from gmdkit.constants.paths.save import SFX_LIBRARY_PATH


@dataclass_decoder(slots=True)
class SFXFile(DelimiterMixin,DataclassDecoderMixin):
    file_id: int
    name: str
    is_folder: bool
    parent_folder: int
    file_size: str
    duration: float = field_decoder(decoder=lambda x: int(x)*0.01,encoder=lambda x: str(round(x*100)))

    # workaround for unsanitized song name
    @classmethod
    def from_tokens(
            cls,
            tokens:Sequence[str],
            **kwargs
            ) -> Self:
        
        for j in range(2, len(tokens)):
            if tokens[j].isdigit():
                tokens[1:j] = [",".join(tokens[1:j])]
                break
            
        return super(SFXFile, cls).from_tokens(tokens,**kwargs)

SFXFile.END_DELIMITER = ";"

class SFXList(ArrayDecoderMixin, ListClass[SFXFile]):
    SEPARATOR = ";"
    KEEP_SEPARATOR = True
    DECODER = SFXFile.from_string
    ENCODER = SFXFile.to_string


@dataclass_decoder(slots=True,from_array=True,separator=",")
class Credits(DelimiterMixin,DataclassDecoderMixin):
    name: str
    website: str

Credits.END_DELIMITER = ";"

class CreditList(ArrayDecoderMixin, ListClass[Credits]):
    SEPARATOR = ";"
    KEEP_SEPARATOR = True
    DECODER = Credits.from_string
    ENCODER = Credits.to_string
    

@dataclass_decoder(slots=True,from_array=True,separator="|")
class SFXLibrary(DefaultPathMixin,FilePathMixin,FileStringMixin,CompressFileMixin,DataclassDecoderMixin):
    files: SFXList = field_decoder(decoder=SFXList.from_string, encoder=SFXList.to_string)
    sfx_credits: CreditList = field_decoder(decoder=CreditList.from_string, encoder=CreditList.to_string)
    
    def _name_fallback_(self):
        return "sfxlibrary"
    
SFXLibrary.COMPRESSED =  True
SFXLibrary.COMPRESSION = "zlib"
SFXLibrary.EXTENSION = "dat"
SFXLibrary.DEFAULT_PATH = SFX_LIBRARY_PATH

if __name__ == "__main__":
    sfx_library = SFXLibrary.from_default_path()