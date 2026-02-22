# Imports
from typing import Any, Optional, Self

# Package Imports
from gmdkit.utils.types import ListClass
from gmdkit.utils.typing import StringDictDecoder, StringDictEncoder
from gmdkit.serialization.mixins import (
    DelimiterMixin,
    ArrayDecoderMixin,
    DataclassDecoderMixin
    )
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.serialization.type_cast import to_string
from gmdkit.models.prop.replay_data.persistent import PersistentData
from gmdkit.models.prop.replay_data.checkpoint import CheckpointData


@dataclass_decoder(slots=True, separator=',', from_array=True)
class ReplayInfo(DataclassDecoderMixin):
    
    end_timestamp: int
    players: int
    game_version: int
    binary: int
    version: int
    persistent_data: Optional[PersistentData] = field_decoder(decoder=PersistentData.from_string,encoder=to_string)

"""
@dataclass_decoder(slots=True,from_array=True,separator=":")
class ReplayEvent(DataclassDecoderMixin):
    event_id: int
    event_data: Optional[Any] = None
"""

@dataclass_decoder(slots=True,from_array=True,separator=",")
class ReplayInput(DataclassDecoderMixin):
    
    delta_step : int
    event: str #Optional[ReplayEvent]


class ReplayEvents(DelimiterMixin, ArrayDecoderMixin, ListClass):
    
    SEPARATOR = ";"
    DECODER = ReplayInput    
    ENCODER = to_string

        