# Imports
from urllib.parse import quote, unquote
from typing import Sequence, Self
import re

# Package Imports
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.serialization.mixins import (
    DataclassDecoderMixin, 
    ArrayDecoderMixin, 
    DelimiterMixin, 
    CompressFileMixin, 
    FilePathMixin,
    FileStringMixin,
    DefaultPathMixin
    )
from gmdkit.utils.types import ListClass
from gmdkit.constants.paths.save import MUSIC_LIBRARY_PATH
 

@dataclass_decoder(slots=True, from_array=True, separator=",")
class Artist(DelimiterMixin, DataclassDecoderMixin):
    artist_id: int
    name: str
    website: str = field_decoder(decoder=unquote,encoder=lambda x: quote(x,safe=""))
    youtube_channel: str = field_decoder(
        decoder=lambda x: 'https://youtube.com/channel/' + x if x else '',
        encoder=lambda x: (m.group(1) if (m := re.search(r"https://youtube\.com/channel/([^/?]+)", x)) else '')
        )
    
Artist.END_DELIMITER = ";"


class ArtistList(DelimiterMixin, ArrayDecoderMixin, ListClass):
    SEPARATOR = ";"
    KEEP_SEPARATOR = True
    DECODER = Artist.from_string
    ENCODER = Artist.to_string


class SongTagList(DelimiterMixin, ArrayDecoderMixin, ListClass):
    START_DELIMITER = "."
    END_DELIMITER = "."
    SEPARATOR = "."
    DECODER = int


class SongArtistList(ArrayDecoderMixin, ListClass):
    SEPARATOR = "."
    GROUP_SIZE = 1
    DECODER = int


@dataclass_decoder(slots=True, from_array=True, separator=",")
class Song(DelimiterMixin, DataclassDecoderMixin):
    song_id: int
    name: str
    artist_id: int
    file_size: int
    duration: int
    tags: SongTagList = field_decoder(decoder=SongTagList.from_string, encoder=SongTagList.to_string)
    music_platform: int
    extra_artists: SongArtistList = field_decoder(decoder=SongArtistList.from_string, encoder=SongArtistList.to_string)
    external_link: str = field_decoder(decoder=unquote,encoder=lambda x: quote(x,safe=""))
    is_new: bool
    priority_order: int
    song_number: int
    
    # workaround for unsanitized song name
    @classmethod
    def from_tokens(
            cls,
            tokens:Sequence[str],
            **kwargs
            ) -> Self:
        
        for j in range(2, len(tokens)):
            if tokens[j].isdigit():
                tokens[1:j] = [",".join(tokens[1:j])]
                break
            
        return super(Song, cls).from_tokens(tokens,**kwargs)
            
Song.END_DELIMITER = ";"


class SongList(DelimiterMixin, ArrayDecoderMixin, ListClass):
    SEPARATOR = ";"
    KEEP_SEPARATOR = True
    DECODER = Song.from_string
    ENCODER = Song.to_string


@dataclass_decoder(slots=True, separator=",")
class Tag(DelimiterMixin, DataclassDecoderMixin):
    tag_id: int
    name: str
    
Tag.END_DELIMITER = ";"


class TagList(DelimiterMixin, ArrayDecoderMixin, ListClass):
    SEPARATOR = ";"
    KEEP_SEPARATOR = True
    DECODER = Tag.from_string
    ENCODER = Tag.to_string


@dataclass_decoder(slots=True, separator="|")
class MusicLibrary(DefaultPathMixin,FilePathMixin,FileStringMixin,CompressFileMixin,DataclassDecoderMixin):
    version: int
    artists: ArtistList = field_decoder(decoder=ArtistList.from_string, encoder=ArtistList.to_string)
    songs: SongList = field_decoder(decoder=SongList.from_string, encoder=SongList.to_string)
    tags: TagList = field_decoder(decoder=TagList.from_string, encoder=TagList.to_string)
    
    def _name_fallback_(self):
        return "musiclibrary"


MusicLibrary.COMPRESSED =  True
MusicLibrary.COMPRESSION = "zlib"
MusicLibrary.EXTENSION = "dat"
MusicLibrary.DEFAULT_PATH = MUSIC_LIBRARY_PATH

if __name__ == "__main__":
    music_library = MusicLibrary.from_default_path()
