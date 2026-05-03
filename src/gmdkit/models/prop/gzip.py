# Imports
from typing import Optional, Self

# Package Imports
from gmdkit.models.object import Object, ObjectList
from gmdkit.serialization.mixins import FileStringMixin
from gmdkit.serialization.functions import decompress_string, compress_string
from gmdkit.models.prop.replay import ReplayInfo, ReplayEvents


LevelObjects = tuple[Object,ObjectList]
ReplayData = tuple[ReplayEvents,ReplayInfo]

class GzipString(FileStringMixin):
    """
    Lazy-loads a gzip compressed string and allows loading and saving it to a decompressed format.

    Parameters
    ----------
    string : str, optional
        The compressed string. Defaults to an empty string.

    Attributes
    ----------
    string : str
        The compressed string.
    decompressed : str or None
        The decompressed string, populated after calling load().
    """

    def __init__(self, string: Optional[str] = None):
        self.string = string or ""
        self.decompressed: Optional[str] = None

    def load(self) -> str:
        """
        Decompress the string and store the result.
        
        Returns
        -------
        str
            The decompressed string.
        """
        self.decompressed = decompress_string(self.string)
        return self.decompressed

    def save(self, string: Optional[str] = None) -> None:
        """
        Compress and store the string.
        
        Parameters
        ----------
        string : str, optional
            If provided, replaces the current decompressed value before saving.
        
        Returns
        -------
        None.
        
        """
        if string is not None:
            self.decompressed = string
        
        if self.decompressed is not None:
            self.string = compress_string(self.decompressed)

    @classmethod
    def from_string(cls, string: str, load: bool = True) -> Self:
        """
        Returns an instance from a compressed string.

        Parameters
        ----------
        string : str
            The compressed string.
        load : bool, optional
            If True, loads before returning the instance. Defaults to True.

        Returns
        -------
        Self
            A new instance.
        """
        new = cls(string)

        if load:
            new.load()

        return new

    def to_string(self, save: bool = True) -> str:
        """
        Return the compressed string.
        
        Parameters
        ----------
        save : bool, optional
            If True, saves the decompressed data before returning. Defaults to True.
        
        Returns
        -------
        str
            The compressed string.
        """
        if save:
            self.save()

        return self.string
    

class ObjectString(GzipString):
    """
    A GzipString that loads level objects.

    Attributes
    ----------
    start : Object
        The level's start object, populated after calling load().
    objects : ObjectList
        The level's objects, populated after calling load().
    """
    
    def load(self) -> LevelObjects:
        """
        Decompresses and parses the level string into level objects.

        Returns
        -------
        LevelObjects
            The level's objects.

        """
        string = super().load()
        
        first, _, remainder = string.partition(";")
        
        self.start = Object.from_string(first)
        self.objects = ObjectList.from_string(remainder)
    
        return self.start, self.objects
    
    
    def save(
            self,
            start: Optional[Object]=None,
            objects: Optional[ObjectList]=None,
            ) -> str:
        """
        Serialize and compress the level data.
        
        Parameters
        ----------
        start : Object, optional
            The start object to serialize. Defaults to the current start attribute.
        objects : ObjectList, optional
            The object list to serialize. Defaults to the current objects attribute.
        
        Returns
        -------
        str
            The compressed string, or the existing string if start or objects are unavailable.
        """
        start = start if start is not None else getattr(self, "start", None)
        objects = objects if objects is not None else getattr(self, "objects", None)
    
        if start is None or objects is None:
            return self.string
    
        string = start.to_string() + objects.to_string()
        super().save(string)
        return self.string
        

class ReplayString(GzipString):
    """
    A GzipString that loads replay events and metadata.
    
    Attributes
    ----------
    start : ReplayInfo
        Replay metadata, populated after calling load().
    events : ReplayEvents
        Replay event data, populated after calling load().
    """
    
    def load(self) -> ReplayData:
        """
        Decompress and parse the replay string into replay events and metadata.
        
        Returns
        -------
        ReplayData
            The level's objects.

        """
        string = super().load()
        
        replay_string, replay_start = string.split("#", 1)
        
        self.metadata = ReplayInfo.from_string(replay_start)
        self.events = ReplayEvents.from_string(replay_string)
            
    def save(
            self,
            metadata: Optional[ReplayInfo]=None,
            events: Optional[ReplayEvents]=None,
            ) -> str:
        """
        Serialize and compress the replay data.
        
        Parameters
        ----------
        start : ReplayInfo, optional
            The replay metadata to serialize. Defaults to the current start attribute.
        events : ReplayEvents, optional
            The replay events to serialize. Defaults to the current events attribute.
        
        Returns
        -------
        str
            The compressed string, or the existing string if start or events are unavailable.
        """
        metadata = metadata if metadata is not None else getattr(self, "metadata", None)
        events = events if events is not None else getattr(self, "events", None)
        
        if metadata is None or events is None:
            return self.string
        
        string = metadata.to_string() + events.to_string()
        
        return super().save(string)