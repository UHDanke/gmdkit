from pathlib import Path
from os import getenv
import sys

# Handle different platforms for GD save location
if sys.platform == "win32":
    LOCAL_PATH = Path(getenv("LOCALAPPDATA", "")) / "GeometryDash"
else:
    LOCAL_PATH = Path.home() / ".local" / "share" / "Steam" / "steamapps" / "common" / "Geometry Dash"

if LOCAL_PATH.exists():
    GAME_MANAGER_PATH = LOCAL_PATH / "CCGameManager.dat"
    LOCAL_LEVELS_PATH = LOCAL_PATH / "CCLocalLevels.dat"
    MUSIC_LIBRARY_PATH = LOCAL_PATH / "musiclibrary.dat"
    SFX_LIBRARY_PATH = LOCAL_PATH / "sfxlibrary.dat"
else:
    GAME_MANAGER_PATH = None
    LOCAL_LEVELS_PATH = None
    MUSIC_LIBRARY_PATH = None
    SFX_LIBRARY_PATH = None