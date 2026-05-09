import pandas as pd
from scripts.build_scripts.utils import tree, build_tree, render_tree, clear_folder

CSV_PATH = "data/csv/object_table.csv"
FILEPATH = "src/gmdkit/casting/list_props.py"
FILEPATH = "src/gmdkit/mappings/obj_id_alias.py"
FOLDERPATH = "src/gmdkit/mappings/obj_id/"

def main():
    # Open object id table
    obj_id_table = pd.read_csv(CSV_PATH)
    obj_id_table = obj_id_table.rename(columns={"object id":"id","gmdkit alias":"alias"})
    obj_alias_ids = obj_id_table[['id','alias']]
    obj_alias_ids=obj_alias_ids.dropna()
    obj_alias_ids.sort_values(by='id')
    paired = tuple(zip(obj_alias_ids['alias'],obj_alias_ids['id']))
    obj_aliases = dict(paired)
    obj_root = tree()
    build_tree(obj_root, obj_aliases)
    # Write mappings
    clear_folder(FOLDERPATH)
    render_tree(obj_root, FOLDERPATH)
    # Write aliasing function
    
    with open(FILEPATH,"w") as f:
        f.write("ALIASES = {")
        for alias, i in paired:
            f.write(f"\n    {i}: {repr(alias)},")
        f.write("\n}")
    

if __name__ == "__main__":
    main()