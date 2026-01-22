from pathlib import Path
from os import PathLike, getenv

LOCAL_PATH = Path(getenv("LOCALAPPDATA")) / "GeometryDash"
GAME_MANAGER_PATH= LOCAL_PATH / "CCGameManager.dat"
LOCAL_LEVELS_PATH = LOCAL_PATH / "CCLocalLevels.dat"
MUSIC_LIBRARY_PATH = LOCAL_PATH / "musiclibrary.dat"
SFX_LIBRARY_PATH = LOCAL_PATH / "sfxlibrary.dat"