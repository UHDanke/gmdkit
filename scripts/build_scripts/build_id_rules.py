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


def normalize_actions(x):
    if not isinstance(x, str):
        return x
    x = x.strip()
    if not x:
        return pd.NA
    return repr({i.strip() for i in x.split(",") if i.strip()})

def render_rule(d):
    parts = []
    keys = ['id_type']
        
    for k, v in d.items():
        if v is not None:
            key_str = k
            val_str = repr(v) if k in keys else str(v)
            if val_str == 'nan': continue
            parts.append(f"{key_str.strip()}={val_str.strip()}")
            
    return "IDRule(" + ", ".join(parts) + ")"


def render_rule_tuple(value):
    tuple_end =  ",)" if len(value) == 1 else ")"
    
    nlist = [
        "    " * 3 + render_rule(item)
        for item in value
    ]
    
    return (
        "(\n"
        + ",\n".join(nlist)
        + "\n"
        + "    " * 2
        + tuple_end
    )

def render_rule_keys(dictionary):
    mlist = []
    
    for key, value in dictionary.items():
        mlist.append(
            "    "
            + f"{key}: "
            + render_rule_tuple(value)
        )
    
    return ',\n'.join(mlist)
        
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
    remap_table["actions"] = remap_table["actions"].apply(normalize_actions)
    remap_table.replace(float("nan"), pd.NA, inplace=True)
    remap_table.replace("TRUE", "True", inplace=True)
    remap_table.replace("FALSE", pd.NA, inplace=True)
    remap_table["object_id"] = remap_table["object_id"].apply(try_convert_int)
    remap_table['min'] = remap_table['min'].apply(try_convert_int)
    remap_table['max'] = remap_table['max'].apply(try_convert_int)
    remap_table["default"] = remap_table['default'].apply(try_convert_int)
    remap_table = remap_table.rename(columns={
        "property_id": "obj_prop_id",
        "type": "id_type",
        "min": "id_min",
        "max": "id_max"
        })          
    
    func_cols = [
        "condition",
        "function",
        "replace",
        "fallback",
        "default",
        "fixed",
        "remappable"
    ]

    unique_functions = set(
        v for v in remap_table[func_cols].values.ravel()
        if (
            pd.notna(v)
            and v not in {"True", "False", True, False}
            and not (
                isinstance(v, str) and (
                v.startswith("lambda")
                or v.strip().lstrip("-").isdigit()
                )   
            )
            and not isinstance(v, int)
        )
    )
    
    if unique_functions:
        id_funcs = "from gmdkit.utils.id_functions import (\n    " + (
            ",\n    ".join(unique_functions)
            ) + "\n)"
    else:
        id_funcs = ""

    unique_types = remap_table["id_type"].dropna().unique().tolist()
    
    result = defaultdict(list)
    
    for _, row in remap_table.iterrows():
        obj_id = row['object_id']
        if pd.isna(obj_id): obj_id = None
        entry = row.drop(labels='object_id').to_dict()
        result[obj_id].append(entry)
        
    with open(TEMPLATE_PATH, "r") as tempfile:
            
        template = tempfile.read()
            
    unique_type_str = repr(set(unique_types))           
    
    base_id_rules = render_rule_tuple(result.pop(None,{}))
    obj_id_rules = render_rule_keys(result)
    
    with open(FILEPATH, "w") as file:
        file.write(template.format(
            rule_funcs=id_funcs,
            unique_types=unique_type_str,
            base_id_rules=base_id_rules,
            obj_id_rules=obj_id_rules,
            ))


if __name__ == "__main__":
    main()