# Imports
from typing import Callable
from collections import Counter
from gmdkit import LevelSave
from gmdkit.serialization.type_cast import get_string
from gmdkit.serialization.functions import decompress_string


def object_string_keys(string:str, collector:Callable):
    
        tokens = decompress_string(string).removesuffix(";").split(";")
        
        for t in tokens:
            keys = t.split(',')[::2]
            collector(keys)



global_counter = Counter()


level_data = LevelSave.from_default_path()

for lvl in level_data["LLM_01"]:
    print(lvl['k2'])
    if 'k4' in lvl:
        object_string_keys(get_string(lvl['k4']),global_counter.update)