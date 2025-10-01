# Imports
import os
import sys
from pathlib import Path

# Package Imports
from gmdkit.models.save import GameSave
from gmdkit.models.prop.gzip import ObjectString
from gmdkit.models.serialization import to_plist_file
from gmdkit.models.object import ObjectList
from gmdkit.functions.object import to_user_coins

save_path = Path("data/dat/")
data_path = Path("data/txt/object_string/official")

output_path = Path("data/gmd/official")
output_original_path = output_path / 'original'
output_copy_path = output_path / 'copy'

output_path.mkdir(parents=True, exist_ok=True)
output_original_path.mkdir(parents=True, exist_ok=True)
output_copy_path.mkdir(parents=True, exist_ok=True)

save_folders = {p.name: p for p in save_path.iterdir() if p.is_dir()}
data_folders = {p.name: p for p in data_path.iterdir() if p.is_dir()}
common = save_folders.keys() & data_folders.keys()

for folder in common:
    
    print(f"Processing folder '{folder}':")
    
    game_data = GameSave.from_file(save_path / folder / 'CCGameManager.dat')
    
    for key, data in game_data["GLM_01"].items():
        
        level_file = data_path / folder / f"{key}.txt"
        
        name = data.get("k2", key)
            
        print(f"Processing level with ID {data['k1']}...")
            
        try:
            with open(level_file, "r", encoding="utf-8", errors="ignore") as f:
                object_string = f.read()
                object_string = object_string.strip().replace("\x00", "")
                data["k4"] = object_string
                to_plist_file(data, output_original_path / f"{name}.gmd")
                
                objects = ObjectList.from_string(object_string, encoded=True)
                objects.apply(to_user_coins)
                object_string = objects.to_string(encoded=True) 
                data["k4"] = object_string
                data.pop('k37',None)
                data.pop('k1')
                data.pop('k38',None)
                data['k21'] = 2
                to_plist_file(data, output_copy_path / f"{name}.gmd")               
                
        except FileNotFoundError:
            print(f"No object string file found, skipping.")
            continue
        
        print(f"Saved {name}.gmd")
