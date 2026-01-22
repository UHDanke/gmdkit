import pandas as pd
from collections import defaultdict

CSV_PATH = "data/csv/remap_table.csv"
TEMPLATE_PATH = "scripts/build_scripts/templates/casting_id_rules.txt"
FILEPATH = "src/gmdkit/casting/id_rules.py"


def try_convert_int(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        return val


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

        
def main():
    remap_table = pd.read_csv(CSV_PATH)
    remap_table = remap_table.dropna(how="all")
    remap_table.columns = remap_table.columns.str.replace(' ', '_')
    remap_table["type"] = remap_table["type"].str.replace(' ', '_')
    remap_table = remap_table.where(pd.notnull(remap_table), None)
    
    # First convert strings to int where possible
    remap_table = remap_table.map(
        lambda x: pd.NA if x is False else x
    )
    remap_table["actions"] = remap_table["actions"].apply(lambda x: repr(x.split(",")).replace(" ", "") if type(x)==str else pd.NA)
    remap_table.replace(float("nan"), pd.NA, inplace=True)
    remap_table.replace("TRUE", "True", inplace=True)
    remap_table.replace("FALSE", pd.NA, inplace=True)
    remap_table["object_id"] = remap_table["object_id"].apply(try_convert_int)
    remap_table['min'] = remap_table['min'].apply(try_convert_int)
    remap_table['max'] = remap_table['max'].apply(try_convert_int)
    remap_table["default"] = remap_table['default'].apply(try_convert_int)
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
        
    
        
    with open(TEMPLATE_PATH, "r") as tempfile:
            
        template = tempfile.read()
            
    unique_type_str = repr(set(unique_types))           
            
    mlist = []
    for key, value in result.items():
        nlist = [
            "    " * 3 + render_rule(item)
            for item in value
        ]
    
        mlist.append(
            "    "
            + f"{key}: [\n"
            + ",\n".join(nlist)
            + "\n"
            + "    " * 2
            + "]"
        )
    
    id_rules = ',\n'.join(mlist)
    
    with open(FILEPATH, "w") as file:
        file.write(template.format(
            unique_types=unique_type_str,
            id_rules=id_rules
            ))


if __name__ == "__main__":
    main()