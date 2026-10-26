# Imports
from typing import Callable, ClassVar, Optional

# Package Imports
from gmdkit.serialization.classes import TokenStream
from gmdkit.serialization.mixins import DelimiterMixin, DataclassDecoderMixin, ArrayDecoderMixin, DictDecoderMixin
from gmdkit.serialization.functions import field_decoder


def nested(cls: type, **kwargs):
    if "default" not in kwargs:
        kwargs.setdefault("default_factory", cls)
    return field_decoder(decoder=cls.from_string, encoder=cls.to_string, **kwargs)


def inline(cls: type, **kwargs):
    if "default" not in kwargs:
        kwargs.setdefault("default_factory", cls)
    return field_decoder(use_streams=True, decoder=cls.from_tokens, encoder=cls.to_tokens, **kwargs)


def _read_rest(stream: TokenStream) -> list:
    return stream.rest()


def _write_rest(value: list, out: list):
    out.extend(value)


def rest(**kwargs):
    kwargs.setdefault("default_factory", list)
    kwargs.setdefault("optional", True)
    return field_decoder(use_streams=True, decoder=_read_rest, encoder=_write_rest, **kwargs)


class ArchiveStruct(DelimiterMixin, DataclassDecoderMixin):
    END_DELIMITER: ClassVar[Optional[str]] = ","


class ArchiveListMixin(DelimiterMixin, ArrayDecoderMixin):
    __slots__ = ()
    SEPARATOR: ClassVar[str] = "|"
    END_DELIMITER: ClassVar[Optional[str]] = "|"
    COUNTED: ClassVar[bool] = True
    DECODER: ClassVar[Optional[Callable]] = int
    ENCODER: ClassVar[Optional[Callable]] = str


class ArchiveDictMixin(DelimiterMixin, DictDecoderMixin):
    SEPARATOR: ClassVar[str] = "|"
    END_DELIMITER: ClassVar[Optional[str]] = "|"
    COUNTED: ClassVar[bool] = True
    DECODER: ClassVar[Optional[Callable]] = staticmethod(lambda k, v: (int(k), int(v)))
    ENCODER: ClassVar[Optional[Callable]] = staticmethod(lambda k, v: (str(k), str(v)))