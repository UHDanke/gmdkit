# Imports
from typing import Any, Optional, Self

# Package Imports
from gmdkit.utils.types import ListClass
from gmdkit.utils.typing import StringDictDecoder
from gmdkit.serialization.mixins import (
    DelimiterMixin,
    ArrayDecoderMixin,
    DataclassDecoderMixin
    )
from gmdkit.utils.enums import ReplayEventID
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.serialization.type_cast import to_string
from gmdkit.models.prop.replay_data.persistent import PersistentData
from gmdkit.models.prop.replay_data.checkpoint import CheckpointData


@dataclass_decoder(slots=True, separator=',', from_array=True)
class ReplayInfo(DataclassDecoderMixin):
    
    timestamp: int
    players: int
    game_version: int
    game_binary: int
    version: int
    persistent_data: PersistentData = field_decoder(decoder=PersistentData.from_string,encoder=to_string)


@dataclass_decoder(slots=True,from_array=True,separator=":",default_optional=True)
class ReplayEvent(DataclassDecoderMixin):
    event_id: ReplayEventID = field_decoder(default=ReplayEventID(0),decoder=ReplayEventID.from_string,encoder=to_string)
    event_data: str = field_decoder(default="")


@dataclass_decoder(slots=True)
class CheckpointEvent(ReplayEvent):
    event_data: CheckpointData = field_decoder(default_factory=CheckpointData,decoder=CheckpointData.from_string,encoder=to_string)


def process_events(string:str):
    
    tokens = string.split(":")
    
    if not tokens:
        return ReplayEvent()
    
    match tokens[0]:
        case "99":
            return CheckpointEvent.from_tokens(tokens)
        case _:
            return ReplayEvent.from_tokens(tokens)


@dataclass_decoder(slots=True,from_array=True,separator=",")
class ReplayInput(DataclassDecoderMixin):
    
    delta_step : int
    event: Any = field_decoder(default_factory=ReplayEvent,optional=True,decoder=process_events,encoder=to_string)

    @classmethod
    def from_string(
            cls, 
            string:str, 
            separator:Optional[str]=None, 
            from_array:Optional[bool]=None,
            decoder:Optional[StringDictDecoder]=None
            ) -> Self:
        
        separator = separator if separator is not None else cls.SEPARATOR
        
        if not string:
            return cls()
        # RobTop PLEASE use a sane serialization format you are getting lost in the commas
        # Checkpoint data also uses commas so maxsplit needs to be specified here.
        tokens = string.split(separator,1)
        
        return cls.from_tokens(
            tokens=tokens,
            from_array=from_array,
            decoder=decoder
            )

class ReplayEvents(DelimiterMixin, ArrayDecoderMixin, ListClass):
    
    SEPARATOR = ";"
    DECODER = ReplayInput.from_string  
    ENCODER = to_string

