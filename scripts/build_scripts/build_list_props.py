import pandas as pd
from scripts.build_scripts.utils import tree, build_tree, render_tree, clear_folder, sort_number

CSV_PATH = "data/csv/list_table.csv"
TEMPLATE_PATH = "scripts/build_scripts/templates/casting_list_props.txt"
FILEPATH = "src/gmdkit/casting/list_props.py"
FOLDERPATH = "src/gmdkit/mappings/list_prop/"

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
                        
                case _: return 'str'
                
        case _: return

def decode_level_props(gd_type, gd_format, key):
    
    match gd_type:
        
        case 'int' | 'integer' | 'number':
            
            match gd_format:
                
                case 'bool': 
                    return 'bool'
                
                case _: 
                    return
                
        case 'float' | 'real':
            return
        
        case 'str' | 'string':
            match gd_format:              
                
                case 'int list':
                    return 'IntList.from_string'
                
                case _:
                    return
                
        case _: return
        
def encode_level_props(gd_type, gd_format, key):
    
    match gd_type:
        
        case 'int' | 'integer' | 'number':
            
            match gd_format:
                
                case 'bool': 
                    return 'int'
        
        case 'float' | 'real':
            return
        
        case 'str' | 'string':
            match gd_format:              
                
                case 'int list':
                    return 'to_string'

                case _: 
                    return
                
        case _: return

def main():
    list_table = pd.read_csv(CSV_PATH)
    list_table['id'] = list_table['id'].apply(lambda x: int(x) if str(x).isdigit() else str(x))
    
    # Compute decode/encode/type for all rows
    list_table['decode'] = list_table.apply(lambda row: decode_level_props(row['type'], row['format'], row['id']), axis=1)
    list_table['encode'] = list_table.apply(lambda row: encode_level_props(row['type'], row['format'], row['id']), axis=1)
    list_table['lvl_type'] = list_table.apply(lambda row: get_lvl_types(row['type'], row['format'], row['id']), axis=1)

    list_class = (
        list_table.dropna(how='all')
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
    
    def gen_dict(column):
        values = [(row['id'], row[column]) 
                  for _, row in list_class.iterrows() if str(row[column]) not in ("nan","None")]
        
        values.sort(key=lambda x: sort_number(x[0]))
        return "\n".join([f"    {repr(x[0])}: {x[1]}," for x in values])
         
    # Generate dictionary entries
    lst_decoders = gen_dict("decode")
    
    lst_encoders = gen_dict("encode")
    
    lst_types = gen_dict("type")


    # Write output file
    with open(FILEPATH, "w") as file:
        file.write(template.format(
            list_decoders=lst_decoders,
            list_encoders=lst_encoders,
            list_types=lst_types
        ))
    
    alias_ids = list_table[['id','alias']]
    alias_ids = alias_ids.dropna()
    aliases = dict(zip(alias_ids['alias'],alias_ids['id']))
    
    root = tree()
    build_tree(root, aliases)
    
    # Write level mappings
    clear_folder(FOLDERPATH)
    render_tree(root, FOLDERPATH)

if __name__ == "__main__":
    main()
    