import pandas as pd

df = pd.read_csv("../data/csv/obj_default_color_table.csv")

df.columns = df.columns.str.strip()

df = df.dropna(subset=["obj_id"])

df['color_1'] = df['color_1'].astype(str).str.strip()
df['color_2'] = df['color_2'].astype(str).str.strip()

df_color_1 = df[df["color_1"] != "None"]
df_color_2 = df[df["color_2"] != "None"]


df_color_1['color_1'] = df_color_1['color_1'].astype(int)
df_color_2['color_2'] = df_color_2['color_2'].astype(int)

color_1_map = dict(zip(df_color_1['obj_id'], df_color_1['color_1']))
color_2_map = dict(zip(df_color_2['obj_id'], df_color_2['color_2']))

with open("../src/gmdkit/defaults/color_default.py","w") as file:
    file.write("COLOR_1_DEFAULT = {\n")
    file.write(",\n".join([f"    {k}: {v}" for k,v in color_1_map.items()]))
    file.write("\n")
    file.write("    }\n")
    file.write("\n\n")
    file.write("COLOR_2_DEFAULT = {\n")
    file.write(",\n".join([f"    {k}: {v}" for k,v in color_2_map.items()]))
    file.write("\n")
    file.write("    }")