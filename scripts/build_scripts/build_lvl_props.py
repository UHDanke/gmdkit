import pandas as pd
from scripts.build_scripts.utils import tree, build_tree, render_tree, clear_folder

CSV_PATH = "data/csv/level_table.csv"
TEMPLATE_PATH = "scripts/build_scripts/templates/casting_lvl_props.txt"
FILEPATH = "src/gmdkit/casting/level_props.py"
FOLDERPATH = "src/gmdkit/mappings/lvl_prop/"

def get_lvl_types(gd_type, gd_format, key):
    
    match gd_type:
        
        case 'int' | 'integer' | 'number':
            
            match gd_format:
                
                case 'bool': 
                    return 'bool'
                
                case _: return 'int'
                
        case 'float' | 'real':
            return 'float'
        
        case 'str' | 'string':
            match gd_format:              
                
                case 'int list':
                    return 'IntList'
                
                case 'gzip':
                    
                    match key:
                        case 'k4':
                            return 'ObjectString'
                        
                        case 'k34':
                            return 'ReplayString'
                        
                case _: return 'str'
                
        case _: return

def decode_level_props(gd_type, gd_format, key):
    
    match gd_type:
        
        case 'int' | 'integer' | 'number':
            
            match gd_format:
                
                case 'bool': 
                    return 'to_bool'
                
                case _: return 'int'
                
        case 'float' | 'real':
            return 'float'
        
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
                        
                case _: return 'str'
                
        case _: return
        
def encode_level_props(gd_type, gd_format, key):
    
    match gd_type:
        
        case 'int' | 'integer' | 'number':
            
            match gd_format:
                
                case 'bool': 
                    return 'from_bool'
        
        case 'float' | 'real':
            return 'from_float'
        
        case 'str' | 'string':
            match gd_format:              
                
                case 'int list':
                    return 'to_string'
                
                case 'gzip':
                    return 'zip_string'
                
                case _: 
                    return 'str'
                
        case _: return

def main():
    level_table = pd.read_csv(CSV_PATH)
    level_table['id'] = level_table['id'].apply(lambda x: int(x) if str(x).isdigit() else str(x))
    
    # Compute decode/encode/type for all rows
    level_table['decode'] = level_table.apply(lambda row: decode_level_props(row['type'], row['format'], row['id']), axis=1)
    level_table['encode'] = level_table.apply(lambda row: encode_level_props(row['type'], row['format'], row['id']), axis=1)
    level_table['lvl_type'] = level_table.apply(lambda row: get_lvl_types(row['type'], row['format'], row['id']), axis=1)
    
    level = level_table[level_table["alias"].str.startswith("level.", na=False)]
    
    level_class = (
        level.dropna(how='all')
        .groupby('id')
        .apply(lambda g: pd.Series({
            'aliases': None if g['alias'].isna().all() else tuple(g['alias']),
            'decode': g['decode'].iloc[0],
            'encode': g['encode'].iloc[0],
            'type': g['lvl_type'].iloc[0],
        }), include_groups=False)
        .reset_index()
        .where(pd.notnull, None)
    )
    
    level_class = level_class.where(pd.notnull(level_class), None)
    
    level_list = level_table[level_table["alias"].str.startswith("list.", na=False)]
    
    list_class = (
        level_list.dropna(how='all')
        .groupby('id')
        .apply(lambda g: pd.Series({
            'aliases': None if g['alias'].isna().all() else tuple(g['alias']),
            'decode': g['decode'].iloc[0],
            'encode': g['encode'].iloc[0],
            'type': g['lvl_type'].iloc[0],
        }), include_groups=False)
        .reset_index()
        .where(pd.notnull, None)
    )
    
    list_class = list_class.where(pd.notnull(list_class), None)
    
    # Read template
    with open(TEMPLATE_PATH, "r") as tempfile:
        template = tempfile.read()
    
    # Generate dictionary entries
    lvl_decoders = "\n".join([
        f"    {repr(row['id'])}: {row['decode']},"
        for _, row in level_class.iterrows()
        if row['decode'] is not None
    ])
    
    lvl_encoders = "\n".join([
        f"    {repr(row['id'])}: {row['encode']},"
        for _, row in level_class.iterrows()
        if row['encode'] is not None
    ])
    
    lvl_types = "\n".join([
        f"    {repr(row['id'])}: {row['type']},"
        for _, row in level_class.iterrows()
        if row['type'] is not None
    ])
    
    lst_decoders = "\n".join([
        f"    {repr(row['id'])}: {row['decode']},"
        for _, row in list_class.iterrows()
        if row['decode'] is not None
    ])
    
    lst_encoders = "\n".join([
        f"    {repr(row['id'])}: {row['encode']},"
        for _, row in list_class.iterrows()
        if row['encode'] is not None
    ])
    
    lst_types = "\n".join([
        f"    {repr(row['id'])}: {row['type']},"
        for _, row in list_class.iterrows()
        if row['type'] is not None
    ])

    
    # Write output file
    with open(FILEPATH, "w") as file:
        file.write(template.format(
            level_decoders=lvl_decoders,
            level_encoders=lvl_encoders,
            level_types=lvl_types,
            list_decoders=lst_decoders,
            list_encoders=lst_encoders,
            list_types=lst_types
        ))
    
    alias_ids = level_table[['id','alias']]
    alias_ids = alias_ids.dropna()
    aliases = dict(zip(alias_ids['alias'],alias_ids['id']))
    
    root = tree()
    build_tree(root, aliases)
    
    # Write level mappings
    clear_folder(FOLDERPATH)
    render_tree(root, FOLDERPATH)

if __name__ == "__main__":
    main()
    