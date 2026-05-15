import pandas as pd
from scripts.build_scripts.utils import tree, build_tree, render_tree, clear_folder, sort_number

CSV_PATH = "data/csv/prop_table.csv"
TEMPLATE_PATH = "scripts/build_scripts/templates/casting_obj_props.txt"
FILEPATH = "src/gmdkit/casting/object_props.py"
FOLDERPATH = "src/gmdkit/mappings/obj_prop/"
CLASSES_FILEPATH = "src/gmdkit/extensions/fielded/object_classes.py"
CLASSES_TEMPLATE_PATH = "scripts/build_scripts/templates/obj_classes.txt"

def match_enum(enum_format):
    match enum_format:
        
        case 'old color':
            return 'enums.OldColor'
        
        case 'easing':
            return 'enums.Easing'
        
        case 'pulse target':
            return 'enums.PulseTarget'
        
        case 'touch mode':
            return 'enums.TouchMode'
        
        case 'instant count mode':
            return 'enums.InstantCountMode'
        
        case 'pickup mode':
            return 'enums.PickupMode'
        
        case 'select axis':
            return 'enums.TargetAxis'
        
        case 'option':
            return 'enums.Option'
        
        case 'camera edge':
            return 'enums.CameraEdge'
        
        case 'arrow direction':
            return 'enums.ArrowDir'
        
        case 'gradient blending':
            return 'enums.GradientBlending'
        
        case 'gradient layer':
            return 'enums.GradientLayer'
        
        case 'select player':
            return 'enums.TargetPlayer'
        
        case 'enter mode':
            return 'enums.EnterMode'
        
        case 'gravity mode':
            return 'enums.GravityMode'
        
        case 'adv follow mode':
            return 'enums.AdvFollowMode'
        
        case 'keyframe ref mode':
            return 'enums.KeyframeRefMode'
        
        case 'ui ref'|'ui x ref'|'ui y ref':
            return 'enums.UIRef'
        
        case 'label special id':
            return 'enums.ItemLabelSpecialID'
        
        case 'label alignment':
            return 'enums.ItemLabelAlignment'
        
        case 'sequence mode':
            return 'enums.SequenceMode'
        
        case 'volume direction':
            return 'enums.VolumeDirection'
        
        case 'item type':
            return 'enums.ItemType'
        
        case 'item operation':
            return 'enums.ItemOperation'
        
        case 'item round op':
            return 'enums.ItemRoundOp'
        
        case 'single color mode':
            return 'enums.SingleColorMode'
        
        case 'speed':
            return 'enums.Speed'
        
        case 'reverb preset':
            return 'enums.ReverbPreset'
        
        case 'keyframe spin':
            return 'enums.KeyframeSpin'
        
        case 'effect special id':
            return 'enums.EffectSpecialCenter'
        
        case 'adv follow init':
            return 'enums.AdvFollowInit'
        
        case 'item sign op':
            return 'enums.ItemSignOp'
        
        case 'stop mode':
            return 'enums.StopMode'
        
        case 'gamemode':
            return 'enums.Gamemode'

        case 'sequence reset':
            return 'enums.SequenceResetType'

        case 'time control stop':
            return 'enums.TimeControlType'
        
        case 'pulse color type':
            return 'enums.PulseColorType'
        
        case _:
            return
    
# Map CSV types to library types
def get_obj_types(gd_type, gd_format, key):
    
    match gd_type:
        
        case 'int' | 'integer' | 'number':
                
            if (enum:=match_enum(gd_format)):
                return enum
            else:
                return 'int'
        
        case 'bool':
            return 'bool'
        
        case 'float' | 'real':
            return 'float'
        
        case 'str' | 'string':
            
            match gd_format:
                
                case 'hsv':
                    return 'HSV'
                
                case 'particle':
                    return 'Particle'
                
                case 'groups' | 'parent_groups':
                    return 'IDList'
                
                case  'events':
                    return "EventList"
                
                case  'sequence' | 'group counts':
                    return 'SequenceList'
                
                case  'weights' | 'group weights':
                    return 'RandomWeightsList'
                
                case 'remaps' |'group remaps':
                    return 'RemapList'
                    
                case 'colors':
                    return 'ColorList'
                
                case 'guidelines':
                    return 'GuidelineList'
                
                case 'color':
                    return 'Color'
                
                case _:
                    return 'str'
        case _:
            return

def decode_obj_props(gd_type, gd_format):
    
    match gd_type:
        
        case 'int' | 'integer' | 'number':
            if (enum:=match_enum(gd_format)):
                return enum
            else:
                return 'int'
        
        case 'bool':
            return 'to_bool'
        
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
                
                case 'groups' | 'parent_groups':
                    return 'IDList.from_string'
                
                case 'events':
                    return "EventList.from_string"
                
                case  'sequence' | 'group counts':
                    return 'SequenceList.from_string'
                
                case  'weights' | 'group weights':
                    return 'RandomWeightsList.from_string'
                
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

def encode_obj_props(gd_type, gd_format):
    
    match gd_type:
        
        case 'bool':
            return 'from_bool'
        
        case 'float' | 'real':
            return 'from_float'
        
        case 'str' | 'string':
            
            match gd_format:
                
                case 'base64':
                    return 'encode_text'
                
                case 'hsv':
                    return 'HSV.to_string'
                
                case 'particle':
                    return 'Particle.to_string'
                
                case 'groups' | 'parent_groups':
                    return 'IDList.to_string'
                
                case 'events':
                    return "EventList.to_string"
                
                case  'sequence' | 'group counts':
                    return 'SequenceList.to_string'
                
                case  'weights' | 'group weights':
                    return 'RandomWeightsList.to_string'
                
                case 'remaps' |'group remaps':
                    return 'RemapList.to_string'
                    
                case 'colors':
                    return 'ColorList.to_string'
                
                case 'guidelines':
                    return 'GuidelineList.to_string'
                
                case 'color':
                    return 'Color.to_string'
                
                case _:
                    return 'str'
        case _:
            return

def get_gmdkit_format(gd_type, gd_format):
    
    t = get_obj_types(gd_type, gd_format, None)
    return t if t is not None else 'str'

def _segments_to_classname(segments: list[str]) -> str:
    
    return "".join(s.strip().title().replace(" ", "").replace("_", "") for s in segments)

def _hoist_common_props(node: dict):
    
    child_keys = [k for k in node if k is not None]

    for ck in child_keys:
        _hoist_common_props(node[ck])

    if len(child_keys) < 2:
        return

    # Build a set of (attr, fmt) present in every child
    def prop_signatures(n):
        return {(attr, fmt) for attr, fmt, _ in n.get(None, [])}

    common_sigs = prop_signatures(node[child_keys[0]])
    for ck in child_keys[1:]:
        common_sigs &= prop_signatures(node[ck])

    if not common_sigs:
        return

    # For each common (attr, fmt), take the prop from the first child
    hoisted: dict[tuple, tuple] = {}
    for ck in child_keys:
        child_props = node[ck].get(None, [])
        remaining = []
        for prop in child_props:
            sig = (prop[0], prop[1])
            if sig in common_sigs:
                hoisted.setdefault(sig, prop)   # keep first occurrence
            else:
                remaining.append(prop)
        node[ck][None] = remaining

    parent_props = node.get(None, [])
    node[None] = parent_props + list(hoisted.values())

def _collect_classes(
    node: dict,
    segments: list[str],
    classes: list[tuple[str, str, list[tuple[str, str, int | str]]]],
):
    
    class_name  = _segments_to_classname(segments)
    parent_name = _segments_to_classname(segments[:-1]) if len(segments) > 1 else "FieldedObject"

    props: list[tuple[str, str, int | str]] = node.get(None, [])
    classes.append((class_name, parent_name, props))

    for child_key in sorted(k for k in node if k is not None):
        _collect_classes(node[child_key], segments + [child_key], classes)

def _insert_prop(root: dict, alias: str, fmt: str, prop_id: int | str):
    
    parts = alias.strip().split('.')
    node = root
    for part in parts[:-1]:
        node = node[part]          # defaultdict auto-creates missing nodes

    leaf_attr = parts[-1].lower()
    if None not in node:
        node[None] = []
    node[None].append((leaf_attr, fmt, prop_id))

def generate_prop_classes(prop_table: pd.DataFrame, filepath: str):
    
    root = tree()   # utils tree() — recursive defaultdict

    for _, row in prop_table.iterrows():
        raw_id    = row['id']
        prop_id   = int(raw_id) if str(raw_id).isdigit() else str(raw_id)
        gd_type   = str(row.get('type',   '')).strip()
        gd_format = str(row.get('format', '')).strip()
        alias     = row.get('alias')

        fmt = get_gmdkit_format(gd_type, gd_format)

        if pd.notna(alias) and str(alias).strip():
            alias_str = str(alias).strip()
            if not any(seg.startswith("M_") for seg in alias_str.split(".")):
                _insert_prop(root, alias_str, fmt, prop_id)

    fielded_object_lines: list[str] = []

    root_props = sorted(root.get(None, []), key=lambda x: sort_number(x[2]))
    for attr, fmt, prop_id in root_props:
        fielded_object_lines.append(f"    {attr}: {fmt} = DictField[{fmt}]({prop_id!r})")
    if not root_props:
        fielded_object_lines.append("    pass")

    _hoist_common_props(root)
    all_classes: list[tuple[str, str, list]] = []
    for child_key in sorted(k for k in root if k is not None):
        _collect_classes(root[child_key], [child_key], all_classes)

    # Emit each subclass at module level
    for class_name, parent_name, props in all_classes:
        fielded_object_lines.append("")
        fielded_object_lines.append("")
        fielded_object_lines.append(f"class {class_name}({parent_name}):")
        body = sorted(props, key=lambda x: sort_number(x[2]))
        for attr, fmt, prop_id in body:
            fielded_object_lines.append(f"    {attr}: {fmt} = DictField[{fmt}]({prop_id!r})")
        if not body:
            fielded_object_lines.append("    pass")

    with open(CLASSES_TEMPLATE_PATH, "r") as f:
        template = f.read()

    with open(filepath, "w") as f:
        f.write(template.format(
            fielded_object="\n".join(fielded_object_lines),
        ))

    print(f"[generate_prop_classes] Written → {filepath}")

def main():
    prop_table = pd.read_csv("data/csv/prop_table.csv")
    prop_table['id'] = prop_table['id'].apply(lambda x: int(x) if str(x).isdigit() else str(x))
    
    prop_class = prop_class = (
        prop_table.dropna(how='all')
        .groupby('id')
        .apply(lambda g: {
            'aliases': (
                None if g['alias'].isna().all()
                else tuple(a for a in g['alias'] if pd.notna(a))
            ),
            'decode': decode_obj_props(g['type'].iloc[0], g['format'].iloc[0]),
            'encode': encode_obj_props(g['type'].iloc[0], g['format'].iloc[0]),
            'type': get_obj_types(g['type'].iloc[0], g['format'].iloc[0], g.index[0]),
        })
        .apply(pd.Series)
        .reset_index()
    )
    
    prop_class = prop_class.where(pd.notnull(prop_class), None)
    
    # Write casting/object_properties.py
    with open(FILEPATH, "w") as file:
        
        with open(TEMPLATE_PATH, "r") as tempfile:
            
            template = tempfile.read()
            
        def gen_dict(column):
            values = [(row['id'], row[column]) 
                      for _, row in prop_class.iterrows() if str(row[column]) not in ("nan","None")]
            
            values.sort(key=lambda x: sort_number(x[0]))
            return "\n".join([f"    {repr(x[0])}: {x[1]}," for x in values])
         
        prop_decoders = gen_dict("decode")
        
        prop_encoders = gen_dict("encode")
        
        prop_types = gen_dict("type")

        file.write(template.format(
            property_decoders=prop_decoders,
            property_encoders=prop_encoders,
            property_types=prop_types
            ))
    
    
    alias_ids = prop_table[['id','alias']]
    alias_ids=alias_ids.dropna()
    aliases = dict(zip(alias_ids['alias'],alias_ids['id']))
    
    root = tree()
    build_tree(root, aliases)
    
    # Write mappings/object_properties.py
    clear_folder(FOLDERPATH)
    render_tree(root, FOLDERPATH)

    generate_prop_classes(prop_table, CLASSES_FILEPATH)

if __name__ == "__main__":
    main()