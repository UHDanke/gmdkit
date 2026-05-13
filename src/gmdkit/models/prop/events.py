# Package Imports
from gmdkit.models.prop.list import IntList
from gmdkit.utils.enums import GameEvents

class EventList(IntList[GameEvents]):
    
    __slots__ = ()
    
    SEPARATOR = "."
    
    DECODER = GameEvents.from_string


