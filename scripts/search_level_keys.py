from gmdkit import GameSave, LevelSave, LevelList, LevelPackList
from gmdkit.models.level import LevelMapping

search_keys = {"k76"}

game_data = GameSave.from_default_path()
level_data = LevelSave.from_default_path()

game_levels = LevelList()
list_levels = LevelList()

def find_levels(data, keys_set, found_levels=None):
    found = 0
    if found_levels is None:
        found_levels = LevelList()

    key_dict = {}    

    if isinstance(data, LevelMapping):
        for lvl_id, lvl in data.items():
            if keys_set & set(lvl.keys()):
                for k, v in lvl.items():
                    if k not in keys_set: continue
                    value_set = key_dict.setdefault(k, set())
                    value_set.add(v)
                if lvl["k76"] < 3:
                    print(lvl["k76"])
                #print(f"LevelMapping {lvl_id}:", {k:v for k,v in lvl.items() if k in keys_set})
                    found_levels.append(lvl)
                    found += 1
                
    elif isinstance(data, (LevelList, LevelPackList)):
        for lvl in data:
            if keys_set & set(lvl.keys()):
                for k, v in lvl.items():
                    if k not in keys_set: continue
                    value_set = key_dict.setdefault(k, set())
                    value_set.add(v)
                print({k:v for k,v in lvl.items() if k in keys_set})
                found_levels.append(lvl)
                found += 1
            
            for k, v in lvl.items():
                if isinstance(v, LevelMapping):
                    find_levels(v, keys_set, found_levels)
            
    elif isinstance(data, dict):
        for k, v in data.items():
            f, _, _ = find_levels(v, keys_set, found_levels)
            if f:
                print(f"^ from {k} ^")
    return found, found_levels, key_dict

find_levels(game_data, search_keys, game_levels)

find_levels(level_data, search_keys, list_levels)