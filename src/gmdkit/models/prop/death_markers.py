# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.serialization.mixins import (
    ArrayDecoderMixin, DictDecoderMixin, DataclassDecoderMixin,
    CompressFileMixin
    )
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.serialization.classes import LazyString, LazyAttr


@dataclass_decoder(slots=True, separator=",", from_array=True)
class DeathMarker(DataclassDecoderMixin):
    x: int = field_decoder(
        decoder=lambda s: int(s)*10,
        encoder=lambda x: str(round(x/10)),
        default=0
        )
    y: int = field_decoder(
        decoder=lambda s: int(s)*10,
        encoder=lambda x: str(round(x/10)),
        default=0
        )
    count: int = 0
    percent: int = 0

class DeathMarkerList(ArrayDecoderMixin,ListClass[DeathMarker]):

    __slots__ = ()

    SEPARATOR = ","
    GROUP_SIZE = 4
    DECODER = DeathMarker.from_tokens
    ENCODER = DeathMarker.to_tokens


class DeathCounts(DictDecoderMixin,DictClass[int,int]):
    SEPARATOR = ","
    DECODER = staticmethod(lambda k, v: (int(k), int(v)))
    ENCODER = staticmethod(lambda k, v: (str(k), str(v)))


@dataclass_decoder(slots=True, separator=",", from_array=True)
class StartPosDeathCount(DataclassDecoderMixin):
    start_percent: int = 0
    percent: int = 0
    count: int = 0

class StartPosDeathCounts(ArrayDecoderMixin, ListClass[StartPosDeathCount]):
    SEPARATOR = ","
    GROUP_SIZE = 3
    DECODER = StartPosDeathCount.from_tokens
    ENCODER = StartPosDeathCount.to_tokens

@dataclass_decoder(slots=True, separator="x", from_array=True)
class Attempt(DataclassDecoderMixin):
    percent: int = 0
    count: int = field_decoder(default=1, optional=True)
    
class AttemptHistory(ArrayDecoderMixin, ListClass[Attempt]):
    SEPARATOR = ","
    DECODER = Attempt.from_string
    ENCODER = Attempt.to_string

@dataclass_decoder(slots=True, separator=",", from_array=True)
class StartPosAttempt(DataclassDecoderMixin):
    start_percent: int = 0
    percent: int = 0

class StartPosAttemptHistory(ArrayDecoderMixin, ListClass[StartPosAttempt]):
    SEPARATOR = ","
    GROUP_SIZE = 2
    DECODER = StartPosAttempt.from_tokens
    ENCODER = StartPosAttempt.to_tokens

@dataclass_decoder(slots=True, separator=":", from_array=True)
class SessionArchive(DataclassDecoderMixin):
    start_timestamp: int
    history: AttemptHistory = field_decoder(
        decoder=AttemptHistory.from_string,
        encoder=AttemptHistory.to_string
        )
    startpos_history: StartPosAttemptHistory = field_decoder(
        decoder=StartPosAttemptHistory.from_string,
        encoder=StartPosAttemptHistory.to_string
        )
    playtime: int
    best_percent: int

class SessionString(CompressFileMixin, ArrayDecoderMixin, ListClass[SessionArchive]):
    SEPARATOR = "|"
    DECODER = SessionArchive.from_string
    ENCODER = SessionArchive.to_string
    COMPRESSED = True
    COMPRESSION = "gzip"

class SessionStringLazy(LazyString):
    PARSER = SessionString
    
    sessions: SessionString = LazyAttr("data")