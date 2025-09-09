TODO README

THIS LIBRARY IS NOT FULLY TESTED, DO NOT EDIT LEVELS WITHOUT BACKUPS.

Basic usage:
```python

# import level
from gmdkit.models.level import Level
# import object property mappings
from gmdkit.mappings import prop_id
# import object functions
import gmdkit.functions.object as obj_func

# open file
level = Level.from_file("example.gmd")

# get inner level properties
start = level.start

# get level objects
obj_list = level.objects

# filter by condition
after_origin = obj_list.where(lambda obj: obj.get(prop_id.x, 0) > 0)

# apply functions, kwargs are filtered for each called function
# ex: obj_func.fix_lighter has replacement as a key argument
after_origin.apply(obj_func.clean_duplicate_groups, obj_func.fix_lighter, replacement=0)
```
