# Imports
from typing import Optional, Self


# Package Imports
from gmdkit.models.object import Object, ObjectList
from gmdkit.serialization.mixins import FileStringMixin
from gmdkit.serialization.functions import decompress_string, compress_string
from gmdkit.models.prop.replay import ReplayInfo, ReplayEvents


LevelObjects = tuple[Object, ObjectList]
ReplayData = tuple[ReplayEvents, ReplayInfo]


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

    def __init__(self, string: str = ""):
        self.string = string
        self.decompressed: Optional[str] = None

    def load(self) -> str:
        """
        Decompress the string and store the result.

        Returns
        -------
        str
            The decompressed string, or an empty string if there is nothing to decompress.
        """
        self.decompressed = decompress_string(self.string) if self.string else ""
        return self.decompressed

    def save(self, string: Optional[str] = None) -> str:
        """
        Compress and store the string.

        Parameters
        ----------
        string : str, optional
            If provided, replaces the current decompressed value before saving.

        Returns
        -------
        str
            The compressed string.
        """
        if string is not None:
            self.decompressed = string

        if self.decompressed is not None:
            self.string = compress_string(self.decompressed) if self.decompressed else ""

        return self.string

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