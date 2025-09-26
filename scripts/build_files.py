import pandas as pd
import shutil
from build_utils import *

# Map CSV types to library types
def decode_obj_props(gd_type, gd_format, key):
    
    match gd_type:
        
        case 'int' | 'integer' | 'number':
            return 'int'
        
        case 'bool':
            return 'lambda x: bool(int(x))'
        
        case 'float' | 'real':
            return 'float'
        
        case 'str' | 'string':
            
            match gd_format:
                
                case 'base64':
                    return 'decode_text'
                
                case 'hsv':
                    return 'HSV.from_string'
                
                case 'particle':
                    return 'Particle.from_string'
                
                case 'groups' | 'parent_groups' | 'events':
                    return 'IDList.from_string'
                
                case  'weights' | 'sequence' | 'group weights' | 'group counts':
                    return 'IntPairList.from_string'
                
                case 'remaps' |'group remaps':
                    return 'RemapList.from_string'
                    
                case 'colors':
                    return 'ColorList.from_string'
                
                case 'guidelines':
                    return 'GuidelineList.from_string'
                
                case 'color':
                    return 'Color.from_string'
                
                case _:
                    return 'str'
        case _:
            return

def encode_obj_props(gd_type, gd_format, key):
    
    match gd_type:
        
        case 'bool':
            return 'lambda x: str(int(x))'
        
        case 'str' | 'string':
            
            match gd_format:
                
                case 'base64':
                    return 'encode_text'
                
                case 'hsv':
                    return 'lambda x: x.to_string()'
                
                case 'particle':
                    return 'lambda x: x.to_string()'
                
                case 'groups' | 'parent_groups' | 'events':
                    return 'lambda x: x.to_string()'
                
                case  'weights' | 'sequence' | 'group weights' | 'group counts':
                    return 'lambda x: x.to_string()'
                
                case 'remaps' |'group remaps':
                    return 'lambda x: x.to_string()'
                    
                case 'colors':
                    return 'lambda x: x.to_string()'
                
                case 'guidelines':
                    return 'lambda x: x.to_string()'
                
                case 'color':
                    return 'lambda x: x.to_string()'
                
                case _:
                    return 'str'
        case _:
            return

def decode_level_props(gd_type, gd_format, key):
    
    match gd_type:
        
        case 'int' | 'integer' | 'number':
            
            match gd_format:
                
                case 'bool': 
                    return 'lambda x: bool(int(x))'
                
                case _: return
        
        case 'str' | 'string':
            match gd_format:              
                
                case 'int list':
                    return 'IntList.from_string'
                
                case 'gzip':
                    
                    match key:
                        case 'k4':
                            return 'ObjectString'
                        
                        case 'k34':
                            return 'ReplayString'
                        
                case _: return
                
        case _: return
        

def encode_level_props(gd_type, gd_format, key):
    
    match gd_type:
        
        case 'int' | 'integer' | 'number':
            
            match gd_format:
                
                case 'bool': 
                    return 'lambda x: str(int(x))'
                
        case 'str' | 'string':
            match gd_format:              
                
                case 'int list':
                    return 'lambda x: x.to_string()'
                
                case 'gzip':
                    return 'lambda x: x.save()'
                
                case _: 
                    return
                
        case _: return



# Open property table
prop_table = pd.read_csv("data/csv/prop_table.csv")
#prop_table['sort_key'] = prop_table['id'].map(sort_id)
#print(prop_table['sort_key'] )
#prop_table = prop_table.sort_values(by='sort_key').reset_index(drop=True)
#prop_table = prop_table.drop(columns=['sort_key'])
prop_table['id'] = prop_table['id'].apply(lambda x: int(x) if str(x).isdigit() else str(x))

prop_class = (
    prop_table.dropna(how='all').groupby('id')
    .apply(lambda g: pd.Series({
        'aliases': None if g['alias'].isna().all() else tuple(g['alias']),
        'decode': decode_obj_props(g['type'].iloc[0], g['format'].iloc[0], g['id'].iloc[0]),
        'encode': encode_obj_props(g['type'].iloc[0], g['format'].iloc[0], g['id'].iloc[0]),
        'type': g['type'].iloc[0],
        'format': g['format'].iloc[0],
    }))
    .reset_index()
)

prop_class = prop_class.where(pd.notnull(prop_class), None)

# Write casting/object_properties.py
file = LineWriter(path="src/gmdkit/casting/object_props.py")
file.write("""
# Package Imports
from gmdkit.models.prop.string import decode_text, encode_text
from gmdkit.models.prop.list import IDList, IntPairList, RemapList
from gmdkit.models.prop.guideline import GuidelineList
from gmdkit.models.prop.hsv import HSV
from gmdkit.models.prop.particle import Particle
from gmdkit.models.prop.color import Color, ColorList
""".strip())
file.write(*[""]*2)
file.write("PROPERTY_DECODERS = {")
file.write(*[
    f"    {repr(row['id'])}: {row['decode']},"
    for _, row in prop_class.iterrows()
    if row['decode'] is not None
])
file.write("}")
file.write(*[""]*2)
file.write("PROPERTY_ENCODERS = {")
file.write(*[
    f"    {repr(row['id'])}: {row['encode']},"
    for _, row in prop_class.iterrows()
    if row['encode'] is not None
])
file.write("}")
file.close()


alias_ids = prop_table[['id','alias']]
alias_ids=alias_ids.dropna()
aliases = dict(zip(alias_ids['alias'],alias_ids['id']))

root = tree()
build_tree(root, aliases)

# Write mappings/object_properties.py
clear_folder("src/gmdkit/mappings/obj_prop/")
render_tree(root, "src/gmdkit/mappings/obj_prop/")

# Open level table
level_table = pd.read_csv("data/csv/level_table.csv")
#level_table['sort_key'] = level_table['id'].map(sort_id)
#level_table = level_table.sort_values(by='sort_key').reset_index(drop=True)
#level_table = level_table.drop(columns=['sort_key'])
level_table['id'] = level_table['id'].apply(lambda x: int(x) if str(x).isdigit() else str(x))

level = level_table[level_table["alias"].str.startswith("level.", na=False)]

level_class = (
    level.dropna(how='all').groupby('id')
    .apply(lambda g: pd.Series({
        'aliases': None if g['alias'].isna().all() else tuple(g['alias']),
        'decode': decode_level_props(g['type'].iloc[0], g['format'].iloc[0], g['id'].iloc[0]),
        'encode': encode_level_props(g['type'].iloc[0], g['format'].iloc[0], g['id'].iloc[0]),
        'type': g['type'].iloc[0],
        'format': g['format'].iloc[0],
    }))
    .reset_index()
)

level_class = level_class.where(pd.notnull(level_class), None)

level_list = level_table[level_table["alias"].str.startswith("list.", na=False)]

list_class = (
    level_list.dropna(how='all').groupby('id')
    .apply(lambda g: pd.Series({
        'aliases': None if g['alias'].isna().all() else tuple(g['alias']),
        'decode': decode_level_props(g['type'].iloc[0], g['format'].iloc[0], g['id'].iloc[0]),
        'encode': encode_level_props(g['type'].iloc[0], g['format'].iloc[0], g['id'].iloc[0]),
        'type': g['type'].iloc[0],
        'format': g['format'].iloc[0],
    }))
    .reset_index()
)

level_class = level_class.where(pd.notnull(level_class), None)
# Write casting/level_properties.py
file = LineWriter(path="src/gmdkit/casting/level_props.py")
file.write("""
# Package Imports
from gmdkit.models.prop.list import IntList
from gmdkit.models.prop.gzip import ObjectString, ReplayString
""".strip())
file.write(*[""]*2)
file.write("LEVEL_DECODERS = {")
file.write(*[
    f"    {repr(row['id'])}: {row['decode']},"
    for _, row in level_class.iterrows()
    if row['decode'] is not None
])
file.write("}")
file.write(*[""]*2)
file.write("LEVEL_ENCODERS = {")
file.write(*[
    f"    {repr(row['id'])}: {row['encode']},"
    for _, row in level_class.iterrows()
    if row['encode'] is not None
])
file.write("}")
file.write(*[""]*2)
file.write("LIST_DECODERS = {")
file.write(*[
    f"    {repr(row['id'])}: {row['decode']},"
    for _, row in list_class.iterrows()
    if row['decode'] is not None
])
file.write("}")
file.write(*[""]*2)
file.write("LIST_ENCODERS = {")
file.write(*[
    f"    {repr(row['id'])}: {row['encode']},"
    for _, row in list_class.iterrows()
    if row['encode'] is not None
])
file.write("}")
file.close()


alias_ids = level_table[['id','alias']]
alias_ids=alias_ids.dropna()
aliases = dict(zip(alias_ids['alias'],alias_ids['id']))

root = tree()
build_tree(root, aliases)

# Write level mappings
clear_folder("src/gmdkit/mappings/lvl_prop/")
render_tree(root, "src/gmdkit/mappings/lvl_prop/")

# Open object id table
obj_id_table = pd.read_csv("data/csv/object_table.csv")


obj_alias_ids = obj_id_table[['id','alias']]
obj_alias_ids=obj_alias_ids.dropna()
obj_alias_ids.sort_values(by='id')
obj_aliases = dict(zip(obj_alias_ids['alias'],obj_alias_ids['id']))
obj_root = tree()
build_tree(obj_root, obj_aliases)
# Write mappings
clear_folder("src/gmdkit/mappings/obj_id/")
render_tree(obj_root, "src/gmdkit/mappings/obj_id/")


remap_table = pd.read_csv("data/csv/remap_table.csv")
remap_table = remap_table.dropna(how="all")

def convert_condition(data):
    
    if isinstance(data, str):
        t = data.split()
    
        return f"lambda obj: obj.get(prop_id.{t[0]},0) {t[1]} {t[2]}"
    
    else:
        return data

def convert_default(data):
    
    if isinstance(data, str):
        
        return f"lambda obj_id: {data}.get(obj_id,0)"

remap_table.columns = remap_table.columns.str.replace(' ', '_')
remap_table["type"] = remap_table["type"].str.replace(' ', '_')
remap_table = remap_table.where(pd.notnull(remap_table), None)

def try_convert_int(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        return val

# First convert strings to int where possible
remap_table["object_id"] = remap_table["object_id"].apply(try_convert_int)
remap_table['min'] = remap_table['min'].astype("Int64")
remap_table['max'] = remap_table['max'].astype("Int64")
remap_table.replace(False, pd.NA, inplace=True)
remap_table = remap_table.rename(columns={
    "property_id": "prop"    
    })

unique_types = remap_table["type"].dropna().unique().tolist()

result = defaultdict(list)

for _, row in remap_table.iterrows():
    obj_id = row['object_id']
    if pd.isna(obj_id): obj_id = None
    entry = row.drop(labels='object_id').to_dict()
    result[obj_id].append(entry)
    
file = LineWriter(path="src/gmdkit/casting/id_rules.py")
file.write("""
# Imports
from typing import Callable
from dataclasses import dataclass

# Package Imports
from gmdkit.mappings import obj_id, obj_prop, color_prop
from gmdkit.defaults.color_default import COLOR_1_DEFAULT, COLOR_2_DEFAULT

@dataclass(frozen=True)
class IDRule:
    type: str
    prop: int
    min: int = -2147483648
    max: int = 2147483647
    remappable: bool = False
    iterable: bool = False
    function: Callable = None
    condition: Callable = None
    default: Callable = None
    replace: Callable = None                
""".strip())
file.write(*[""]*2)
file.write(f"ID_TYPES = {repr(unique_types)}")
file.write(*[""]*2)
file.write("ID_RULES = {")

def render_rule(d):
    parts = []
    keys = ['type']
    
    for k, v in d.items():
        if v is not None:
            key_str = k
            val_str = repr(v) if k in keys else str(v)
            if val_str == 'nan': continue
            parts.append(f"{key_str}={val_str}")
    return "IDRule(" + ", ".join(parts) + ")"


mlist = []
for key, value in result.items():
    nlist = []
    for item in value:
        nlist.append("    "*3+render_rule(item))
    mlist.append("    "+f"{key}: "+"[\n"+',\n'.join(nlist)+"\n"+"    "*2+"]")

file.write(',\n'.join(mlist))

file.write("    "+"}")
file.close()
