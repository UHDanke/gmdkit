# Imports
import os
import sys
from pathlib import Path

# Package Imports
from gmdkit.models.save import GameSave
from gmdkit.models.serialization import to_plist_file
from gmdkit.models.object import ObjectList
from gmdkit.functions.object import to_user_coins


manual_path = os.getenv("GEOMETRY_DASH_PATH")
dont_convert_coins = os.getenv("DONT_CONVERT_COINS")

STEAM_PATHS = [
    Path("C:/Program Files (x86)/Steam/steamapps/common"),
    Path("D:/SteamLibrary/steamapps/common"),
    Path("E:/SteamLibrary/steamapps/common"),
]

GAME_FOLDER = "Geometry Dash"

if manual_path:
    base_path = Path(manual_path)
else:
    base_path = next((p / GAME_FOLDER for p in STEAM_PATHS if (p / GAME_FOLDER).exists()), None)

if base_path is None:
    print("Could not find Geometry Dash installation. Please set GEOMETRY_DASH_PATH manually.")
    sys.exit(1)

resources_path = base_path / "Resources" / "levels"
output_path = Path("data/gmd/official")
output_path.mkdir(parents=True, exist_ok=True)

game_data = GameSave.from_file()

seen = set()

for key, data in game_data["GLM_01"].items():
    
    level_file = resources_path / f"{key}.txt"

    name = data.get("k2", key)
    
    if name in seen: name = key
    
    seen.add(name)
        
    print(f"Processing level with ID {data['k1']}")
        
    try:
        with open(level_file, "r", encoding="utf-8", errors="ignore") as f:
            object_string = f.read()
            object_string = object_string.strip().replace("\x00", "")
            
            if not dont_convert_coins:
                objects = ObjectList.from_string(object_string, encoded=True)
                objects.apply(to_user_coins)
                object_string = objects.to_string(encoded=True)           
            
            data["k4"] = object_string
    
    except FileNotFoundError:
        print(f"No object string file found, skipping.")
        continue
    
    print(f"Saved {name}.gmd")
    out_file = output_path / f"{name}.gmd"
    
    to_plist_file(data, out_file)
