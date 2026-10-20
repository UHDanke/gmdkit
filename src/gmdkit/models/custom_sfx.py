# Imports
from typing import Self

# Package Imports
from gmdkit.utils.types import ListClass
from gmdkit.serialization.mixins import (
    ArrayDecoderMixin, DataclassDecoderMixin, DelimiterMixin, FilePathMixin
    )
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.serialization.type_cast import decode_text, encode_text
from gmdkit.models.prop.list import IntList


@dataclass_decoder(slots=True, separator=",", from_array=True)
class CustomSFXFolder(DataclassDecoderMixin):
    custom_id: int = 0
    parent_id: int = 1
    name: str = field_decoder(default="", decoder=decode_text, encoder=encode_text)

@dataclass_decoder(slots=True, separator=",", from_array=True)
class CustomSFX(DataclassDecoderMixin):
    custom_id: int = 0
    parent_id: int = 1
    sfx_id: int = 0
    name: str = field_decoder(default="", decoder=decode_text, encoder=encode_text)

class CustomSFXFolderList(DelimiterMixin, ArrayDecoderMixin, ListClass[CustomSFXFolder]):

    __slots__ = ()

    SEPARATOR = ";"
    END_DELIMITER = ";"
    DECODER = CustomSFXFolder.from_string
    ENCODER = CustomSFXFolder.to_string

class CustomSFXList(DelimiterMixin, ArrayDecoderMixin, ListClass[CustomSFX]):

    __slots__ = ()

    SEPARATOR = ";"
    END_DELIMITER = ";"
    DECODER = CustomSFX.from_string
    ENCODER = CustomSFX.to_string


@dataclass_decoder(slots=True, separator="|", from_array=True)
class CustomSFXLibrary(FilePathMixin, DataclassDecoderMixin):
    version: int = 1
    next_id: int = 2
    folders: CustomSFXFolderList = field_decoder(
        default_factory=CustomSFXFolderList,
        decoder=CustomSFXFolderList.from_string,
        encoder=CustomSFXFolderList.to_string
        )
    sounds: CustomSFXList = field_decoder(
        default_factory=CustomSFXList,
        decoder=CustomSFXList.from_string,
        encoder=CustomSFXList.to_string
        )

    @classmethod
    def from_base64(cls, string: str, **kwargs) -> Self:
        return cls.from_string(decode_text(string), **kwargs)

    def to_base64(self, **kwargs) -> str:
        return encode_text(self.to_string(**kwargs))

    def path(self, node_id: int) -> list[str]:
        parents = {f.id: f for f in self.folders}
        parents.update({s.id: s for s in self.sounds})
        names = []
        node = parents.get(node_id)
        while node is not None:
            names.append(node.name)
            node = parents.get(node.parent_id)
        return names[::-1]

CustomSFXLibrary.EXTENSION = "gdsfx"

class CustomSFXPath(ArrayDecoderMixin, ListClass[str]):
    
    __slots__ = ()

    SEPARATOR = "/"
    DECODER = decode_text
    ENCODER = encode_text

@dataclass_decoder(slots=True, separator=":", from_array=True)
class CustomSFXMapping(DataclassDecoderMixin):
    sfx_id: int = 0
    custom_id: int = 0
    path: CustomSFXPath = field_decoder(
        default_factory=CustomSFXPath,
        decoder=CustomSFXPath.from_string,
        encoder=CustomSFXPath.to_string
        )

class CustomSFXMappingList(ArrayDecoderMixin, ListClass[CustomSFXMapping]):

    __slots__ = ()

    SEPARATOR = "|"
    DECODER = CustomSFXMapping.from_string
    ENCODER = CustomSFXMapping.to_string


@dataclass_decoder(slots=True, separator="|", from_array=True)
class CustomSFXMapString(DataclassDecoderMixin):

    version: int = 1
    mappings: CustomSFXMappingList = field_decoder(
        default_factory=CustomSFXMappingList,
        decoder=CustomSFXMappingList.from_string,
        encoder=CustomSFXMappingList.to_string
        )

CustomSFXMapString.MAX_SPLIT = 1


class CustomSFXFolderIDList(IntList):

    __slots__ = ()

    SEPARATOR = "|"