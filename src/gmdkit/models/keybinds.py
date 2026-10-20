# Imports
from typing import Self

# Package Imports
from gmdkit.utils.types import DictClass
from gmdkit.serialization.mixins import (
    DictDecoderMixin, DataclassDecoderMixin, FilePathMixin
    )
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.models.pro.controls import InputKeyList


class KeybindDict(DictDecoderMixin, DictClass[int, InputKeyList]):
    SEPARATOR = "|"
    PAIR_SEPARATOR = ":"
    SORT_KEYS = True
    DECODER = staticmethod(lambda k, v: (int(k), InputKeyList.from_string(v)))
    ENCODER = staticmethod(lambda k, v: (str(k), ",".join(map(str, v))))


@dataclass_decoder(slots=True, separator=";", from_array=True)
class KeybindFile(FilePathMixin, DataclassDecoderMixin):
    file_version: int = 1
    binds: KeybindDict = field_decoder(
        default_factory=KeybindDict,
        decoder=KeybindDict.from_string,
        encoder=KeybindDict.to_string
        )
    binds_version: int = 2

KeybindFile.MAX_SPLIT = 2
KeybindFile.EXTENSION = "gdkb"