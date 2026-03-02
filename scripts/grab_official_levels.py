# Imports
from pathlib import Path

# Package Imports
from gmdkit import GameSave, ObjectString
from gmdkit.mappings import lvl_prop
from gmdkit.functions.object import to_user_coins

save_path = Path("data/dat/")
data_path = Path("data/txt/object_string/official")

output_path = Path("data/gmd/official")

output_path.mkdir(parents=True, exist_ok=True)

save_folders = {p.name: p for p in save_path.iterdir() if p.is_dir()}
data_folders = {p.name: p for p in data_path.iterdir() if p.is_dir()}
common = save_folders.keys() & data_folders.keys()

for folder in common:
    
    print(f"Processing folder '{folder}':")
    
    game_data = GameSave.from_file(save_path / folder / 'CCGameManager.dat')
    
    for key, data in game_data["GLM_01"].items():
        
        level_file = data_path / folder / f"{key}.txt"
            
        print(f"Processing level with ID {data['k1']}...")
            
        try:
            
            data[lvl_prop.OBJECT_STRING] = ObjectString.from_file(level_file,encoding="latin-1")
            
            data.objects.apply(to_user_coins)
            
            data[lvl_prop.TYPE] = 2
            
            data.to_file(output_path)
        except FileNotFoundError:
            print("No object string file found, skipping.")
            continue
        
        print(f"Saved {data[lvl_prop.NAME]}.gmd")
