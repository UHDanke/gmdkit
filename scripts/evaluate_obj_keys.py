from gmdkit.models.prop.gzip import GzipString
# Imports
from typing import Optional
from collections import Counter
from gmdkit import LevelSave
from gmdkit.serialization.type_cast import get_string

class KeyGrabber(GzipString):
    
    def load(
            self, string:Optional[str]=None,
            counter:Optional[Counter]=None,
            ):
        
        if string is None:
            string = super().load()
        
        tokens = string.removesuffix(";").split(";")
        
        counter = Counter() if counter is None else counter
        self.counter = counter
        
        for t in tokens:
            keys = t.split(',')[::2]
            counter.update(keys)
        
        return self.counter
    

global_counter = Counter()


level_data = LevelSave.from_default_path()

for lvl in level_data["LLM_01"]:
    print(lvl['k2'])
    if 'k4' in lvl:
        key_grabber = KeyGrabber(get_string(lvl['k4']))
        key_grabber.load(counter=global_counter)