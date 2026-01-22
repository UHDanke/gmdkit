# Imports
from pathlib import Path

# Package Imports
from gmdkit.models.save.level_list import LevelSave
from gmdkit.mappings import lvl_prop, lvl_save


def extract_levels(
        level_save:LevelSave,
        output_folder,
        use_folders:bool=False,
        folder_names:dict|None=None
        ):
    
    output_folder = Path(output_folder)
    folder_names = folder_names or {}
    digit_count = len(str(len(level_save[lvl_save.LEVELS])))
    
    for i, lvl in enumerate(level_save[lvl_save.LEVELS]):
        if use_folders:
            folder = lvl.get(lvl_prop.level.LEVEL_FOLDER, 0)
            subfolder = folder_names.get(folder, folder)
            out_dir = output_folder / str(subfolder)
            out_dir.mkdir(parents=True, exist_ok=True)
        else:
            out_dir = output_folder
        lvl_name = lvl.get(lvl_prop.level.NAME, "Unnamed")
        out_dir /= f"{i:0{digit_count}d} {lvl_name}.gmd"
        print(out_dir)
        i+=1
        lvl.to_file(path=out_dir,save=False)
