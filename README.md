![PyPI](https://img.shields.io/pypi/v/gmdkit?style=flat-square)
![Python](https://img.shields.io/pypi/pyversions/gmdkit?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

# GMD Toolkit

Python toolkit for modifying & creating Geometry Dash plist files, including gmd & gmdl (GDShare level & level list export) and the encoded dat format (GD savefiles).


> [!CAUTION]
> There are no safety checks or warnings when  modifying levels or save files. You should always keep backups or save copies of any file you edit. Avoid editing in-place where possible.

> [!NOTE]
> Editing levels or save files does not ensure safe round-trip if nothing was changed. This library saves level objects slightly differently and discards unknown characters if they cannot be resolved.


## Installation

Install the latest release from PyPI:

```bash
pip install gmdkit
```

Install the latest development version from GitHub:

```bash
pip install git+https://github.com/UHDanke/gmdkit.git
```

Clone and install in editable mode:

```bash
git clone https://github.com/UHDanke/gmdkit.git
cd gmdkit
pip install -e .
```

## Basic Usage

Importing, modifying a level and saving it:

```python
# import level
from gmdkit.models.level import Level

# import object
from gmdkit.models.object import Object

# import property mappings
from gmdkit.mappings import obj_prop

# import object functions
import gmdkit.functions.object as obj_func

# open file
level = Level.from_file("example.gmd")

# get inner level properties
start = level.start

# get level objects as an ObjectList()
# object lists subclass list() so they can use all list methods alongside the ones defined by ListClass
# level.objects WILL throw AttributeError() if the level lacks an object string,
# or if you passed load = False to Level.from_file(), which skips loading objects
# LevelSave by default does not load the objects of levels
# so for any level you want to edit the objects of you must call level.load() first
obj_list = level.objects

# filter by condition
after_origin = obj_list.where(lambda obj: obj.get(obj_prop.X, 0) > 0)

# apply functions, kwargs are filtered for each called function
# ex: obj_func.fix_lighter has 'replacement' as a key argument
after_origin.apply(obj_func.clean_duplicate_groups, obj_func.fix_lighter, replacement=0)

# create new object
new_obj = Object.default(1)
# set properties of object
# objects subclass dict() so they can use all dict methods alongside the ones defined by DictClass
new_obj.update(
  {
    obj_prop.X: 100,
    obj_prop.Y: 200,
    obj_prop.SCALE_X: 2,
    obj_prop.SCALE_Y: 2
  }
)

# append object to the level's object list
# can also be done directly to level.objects or level['k4'].objects (which level.objects references)
# lvl_prop.level.OBJECT_STRING also maps to 'k4'
obj_list.append(new_obj)
    
# export level
level.to_file("example.gmd")
```

## Documentation (WIP)

You can find the work-in-progress documentation at:  

https://UHDanke.github.io/gmdkit/
