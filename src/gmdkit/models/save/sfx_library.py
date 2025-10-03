# Imports
from dataclasses import dataclass
from urllib.parse import quote, unquote

# Package Imports
from gmdkit.models.serialization import DataclassDecoderMixin, ArrayDecoderMixin, DelimiterMixin, LoadFileMixin, dict_cast
from gmdkit.models.types import ListClass
from gmdkit.constants.paths import SFX_LIBRARY_PATH


@dataclass(slots=True)
class SFXFile(DelimiterMixin, DataclassDecoderMixin):
    file_id: int
    name: str
    is_folder: bool
    parent_folder: int
    file_size: str
    duration: float
    
SFXFile.DECODER = staticmethod(dict_cast(
    {
     'file_id': int,
     'sfx_credits': str,
     'is_folder': lambda x: bool(int(x)),
     'parent_folder': int,
     'file_size': int,
     'duration': lambda x: int(x)*0.01
     }
    ))

SFXFile.ENCODER = staticmethod(dict_cast(
    {
     'file_id': str,
     'sfx_credits': str,
     'is_folder': lambda x: str(int(x)),
     'parent_folder': str,
     'file_size': str,
     'duration': lambda x: str(round(x*100))
     }
    ))

def _temp_sfx_from_string(string):
    # workaround for unsanitized song title
    try:
        return SFXFile.from_string(string)
    except:
        print(string)
        return None

class SFXList(DelimiterMixin, ArrayDecoderMixin, ListClass):
    SEPARATOR = ";"
    END_SEP = True
    DECODER = _temp_sfx_from_string
    ENCODER = staticmethod(lambda x: x.to_string())


@dataclass(slots=True)
class Credits(DelimiterMixin, DataclassDecoderMixin):
    name: str
    website: str
    
class CreditList(SFXList):
    DECODER = Credits.from_string


@dataclass(slots=True)
class SFXLibrary(LoadFileMixin,DataclassDecoderMixin):
    files: str
    sfx_credits: str
    
SFXLibrary.SEPARATOR = "|"    
SFXLibrary.DEFAULT_PATH = SFX_LIBRARY_PATH
SFXLibrary.COMPRESSION = "zlib"
SFXLibrary.DECODER = staticmethod(dict_cast(
    {
     'files': SFXList.from_string,
     'sfx_credits': CreditList.from_string,
     }
    ))


if __name__ == "__main__":
    sfx_library = SFXLibrary.from_file()