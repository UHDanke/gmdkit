# Imports
from typing import Any, Optional

# Package Imports
from gmdkit.utils.types import ListClass
from gmdkit.serialization.mixins import (
    DelimiterMixin,
    ArrayDecoderMixin,
    DataclassDecoderMixin
    )
from gmdkit.serialization.decorators import dataclass_decoder, field_decoder
from gmdkit.serialization.type_cast import to_string
from gmdkit.models.prop.replay_data.persistent import PersistentData
from gmdkit.models.prop.replay_data.checkpoint import CheckpointData

@dataclass_decoder(slots=True, separator=',', list_format=True)
class ReplayInfo(DataclassDecoderMixin):
    
    end_timestamp: int
    players: int
    game_version: int
    binary: int
    version: int
    persistent_data: Optional[PersistentData] = field_decoder(decoder=PersistentData.from_string,encoder=to_string)


class ReplayInput:
    
    start: bool
    delta_step : int
    event_id : int
    event_data: Any
    
    @classmethod
    def from_string(cls, string:str):
        
        start = string.startswith("-")
        t = string.removeprefix("-").split(",")
        delta_step = int(t[0])

        if len(t) == 1:
            event_id = 0
            event_data = None
        else:
            t2 = t[1].split(":")
            event_id = int(t2[0])
            
            if len(t2) == 1:
                event_data = None
                
            else:
                match event_id: 
                    case 99:
                        event_data = CheckpointData.from_string(t2[1])
                    case _:
                        event_data = t2[1]
            
        return cls(
            start,
            delta_step,
            event_id,
            event_data
            )
    
    
    def to_string(self):
        
        if self.start:
            string = "-"
        else:
            string = ""
            
        string += str(self.delta_step)
        
        if self.event_id:
            string += f",{self.event_id}"
            
            if self.event_data:
                string += ":"
                
                match self.event_id:
                    case 99:
                        string += self.event_data.to_string()
                    case _:
                        string += self.event_data
                
        return string

class ReplayEvents(DelimiterMixin, ArrayDecoderMixin, ListClass):
    
    SEPARATOR = ";"
    DECODER = ReplayInput    
    ENCODER = to_string

        