from gmdkit import GameSave, LevelSave, LevelList, LevelPackList
from gmdkit.models.level import LevelMapping

search_keys = {"k115","k116","k117","k118","k119","k120","k121","k122","k123","k124","k125"}

game_data = GameSave.from_default_path()
level_data = LevelSave.from_default_path()

game_levels = LevelList()
list_levels = LevelList()

def find_levels(data, keys_set, found_levels=None):
    if found_levels is None:
        found_levels = LevelList()

    
    if isinstance(data, LevelMapping):
        for lvl_id, lvl in data.items():
            if keys_set & set(lvl.keys()):
                print(f"LevelMapping {lvl_id}:", {k:v for k,v in lvl.items() if k in keys_set})
                found_levels.append(lvl)
                
    elif isinstance(data, (LevelList, LevelPackList)):
        for lvl in data:
            if keys_set & set(lvl.keys()):
                print({k:v for k,v in lvl.items() if k in keys_set})
                found_levels.append(lvl)
            
            for k, v in lvl.items():
                if isinstance(v, LevelMapping):
                    find_levels(v, keys_set, found_levels)
            
    elif isinstance(data, dict):
        for k, v in data.items():
            find_levels(v, keys_set, found_levels)

    return found_levels

find_levels(game_data, search_keys, game_levels)

find_levels(level_data, search_keys, list_levels)