# Imports
from dataclasses import dataclass
from urllib.parse import quote, unquote
import re

# Package Imports
from gmdkit.models.serialization import DataclassDecoderMixin, ArrayDecoderMixin, DelimiterMixin, LoadFileMixin, dict_cast
from gmdkit.models.types import ListClass
from gmdkit.constants.paths import MUSIC_LIBRARY_PATH, SFX_LIBRARY_PATH
 

@dataclass(slots=True)
class Artist(DelimiterMixin, DataclassDecoderMixin):
    artist_id: int
    name: str
    website: str
    youtube_channel: str
    
Artist.END_DELIMITER = ";"
Artist.DECODER = staticmethod(dict_cast(
    {
     'artist_id': int,
     'name': str,
     'website': lambda x: unquote(x),
     'youtube_channel': lambda x: 'https://youtube.com/channel/' + x if x else ''
     }
    ))
    
Artist.ENCODER = staticmethod(dict_cast(
    {
     'artist_id': str,
     'name': str,
     'website': lambda x: quote(x,safe=""),
     'youtube_channel': lambda x: (m.group(1) if (m := re.search(r"https://youtube\.com/channel/([^/?]+)", x)) else '')

     }
    ))

class ArtistList(DelimiterMixin, ArrayDecoderMixin, ListClass):
    SEPARATOR = ";"
    END_SEP = True
    DECODER = Artist.from_string
    ENCODER = staticmethod(lambda x: x.to_string())


class SongTagList(DelimiterMixin, ArrayDecoderMixin, ListClass):
    START_DELIMITER = "."
    END_DELIMITER = "."
    SEPARATOR = "."
    DECODER = int
    
class SongArtistList(ArrayDecoderMixin, ListClass):
    SEPARATOR = "."
    GROUP_SIZE = 1
    DECODER = int

@dataclass(slots=True)
class Song(DelimiterMixin, DataclassDecoderMixin):
    song_id: int
    name: str
    artist_id: int
    file_size: int
    duration: int
    tags: SongTagList
    music_platform: int
    extra_artists: SongArtistList
    external_link: str
    is_new: bool
    priority_order: int
    song_number: int

Song.END_DELIMITER = ";"
Song.STRICT = False
Song.DECODER = staticmethod(dict_cast(
    {
     'song_id': int,
     'name': str,
     'artist_id': int,
     'filesize': int,
     'duration': int,
     'tags': SongTagList.from_string,
     'music_platform': int,
     'extra_artists': SongArtistList.from_string,
     'external_link': lambda x: unquote(x),
     'is_new': lambda x: bool(int(x)),
     'priority_order': int,
     'song_number': int
     }
    ))
    
Song.ENCODER = staticmethod(dict_cast(
    {
     'song_id': str,
     'name': str,
     'artist_id': str,
     'filesize': str,
     'duration': str,
     'tags': lambda x: x.to_string(),
     'music_platform': str,
     'extra_artists': lambda x: x.to_string(),
     'external_link': lambda x: quote(x,safe=""),
     'is_new': lambda x: str(int(x)),
     'priority_order': str,
     'song_number': str
     }
    ))

def _temp_song_from_string(string):
    # workaround for unsanitized song title
    try:
        return Song.from_string(string)
    except:
        print(string)
        return None

class SongList(ArtistList):
    #DECODER = Song.from_string
    DECODER = staticmethod(_temp_song_from_string)


@dataclass(slots=True)
class Tag(DelimiterMixin, DataclassDecoderMixin):
    tag_id: int
    name: str

Tag.SEPARATOR = ","
Tag.END_DELIMITER = ";"
    
class TagList(ArtistList):
    DECODER = Tag.from_string


@dataclass(slots=True)
class MusicLibrary(LoadFileMixin,DataclassDecoderMixin):
    version: int
    artists: ArtistList
    songs: SongList
    tags: TagList
            
        
MusicLibrary.SEPARATOR = "|"    
MusicLibrary.DEFAULT_PATH = MUSIC_LIBRARY_PATH
MusicLibrary.COMPRESSION = "zlib"
MusicLibrary.DECODER = staticmethod(dict_cast(
    {
     'version': int,
     'artists': ArtistList.from_string,
     'songs': SongList.from_string,
     'tags': TagList.from_string
     }
    ))
    
MusicLibrary.ENCODER = staticmethod(dict_cast(
    {
     'version': str,
     'artists': lambda x: x.to_string(),
     'songs': lambda x: x.to_string(),
     'tags': lambda x: x.to_string()
     }
    ))


if __name__ == "__main__":
    music_library = MusicLibrary.from_file()
