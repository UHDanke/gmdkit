# Imports
from dataclasses import field

# Package Imports
from gmdkit.serialization.mixins import ArrayDecoderMixin, DelimiterMixin, CompressFileMixin
from gmdkit.serialization.decorators import dataclass_decoder
from gmdkit.serialization.type_cast import to_string
from gmdkit.serialization.types import ListClass
from gmdkit.constants.paths.save import SFX_LIBRARY_PATH


@dataclass_decoder(slots=True)
class SFXFile(DelimiterMixin):
    file_id: int
    name: str
    is_folder: bool
    parent_folder: int
    file_size: str
    duration: float = field(metadata={"decoder":lambda x: int(x)*0.01,"encoder":lambda x: str(round(x*100))})
    

def _temp_sfx_from_string(string):
    # workaround for unsanitized song title
    try:
        return SFXFile.from_string(string)
    except:
        print(string)
        return None

class SFXList(DelimiterMixin, ArrayDecoderMixin, ListClass):
    SEPARATOR = ";"
    KEEP_SEP = True
    DECODER = _temp_sfx_from_string
    ENCODER = staticmethod(to_string)


@dataclass_decoder(slots=True)
class Credits(DelimiterMixin):
    name: str
    website: str
    
class CreditList(SFXList):
    DECODER = Credits.from_string

@dataclass_decoder(slots=True, separator="|")
class SFXLibrary(CompressFileMixin):
    files: str = field(metadata={"decoder":SFXList.from_string,"encoder":to_string})
    sfx_credits: str = field(metadata={"decoder":CreditList.from_string,"encoder":to_string})
    
SFXLibrary.DEFAULT_PATH = SFX_LIBRARY_PATH
SFXLibrary.COMPRESSION = "zlib"


if __name__ == "__main__":
    sfx_library = SFXLibrary.from_file()