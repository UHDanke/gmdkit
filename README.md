# GMD Toolkit

![PyPI](https://img.shields.io/pypi/v/gmdkit?style=flat-square)
![Python](https://img.shields.io/pypi/pyversions/gmdkit?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

Python toolkit for modifying & creating Geometry Dash plist files, including gmd, gmdl and the encoded dat format.


> [!CAUTION]
> There are no safety checks or warnings when  modifying levels or save files. You should always keep backups or save copies of any file you edit. Avoid editing in-place where possible.

> [!NOTE]
> Editing levels or save files does not ensure safe round-trip if nothing was changed. The library saves level objects slightly differently and discards unknown characters if they cannot be resolved.


# Installation

Install the latest release from PyPI:

```bash
pip install projectname
```

Install the latest development version from GitHub:

```bash
pip install git+https://github.com/yourusername/reponame.git
```

Clone and install in editable mode:

```bash
git clone https://github.com/yourusername/reponame.git
cd reponame
pip install -e .
```

# Basic Usage

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
 # Documentation