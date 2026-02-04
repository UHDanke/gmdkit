import pandas as pd
from scripts.build_scripts.utils import tree, build_tree, render_tree, clear_folder, sort_number

CSV_PATH = "data/csv/prop_table.csv"
TEMPLATE_PATH = "scripts/build_scripts/templates/casting_obj_props.txt"
FILEPATH = "src/gmdkit/casting/object_props.py"
FOLDERPATH = "src/gmdkit/mappings/obj_prop/"


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
            return 'enums.SelectAxis'
        
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
            return 'enums.SelectPlayer'
        
        case 'enter mode':
            return 'enums.EnterMode'
        
        case 'gravity mode':
            return 'enums.GravityMode'
        
        case 'adv follow mode':
            return 'enums.AdvFollowMode'
        
        case 'keyframe ref mode':
            return 'enums.KeyframeRefMode'
        
        case 'ui x ref':
            return 'enums.UIRefX'
        
        case 'ui y ref':
            return 'enums.UIRefY'
        
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
                
                case  'weights' | 'sequence' | 'group weights' | 'group counts':
                    return 'IntPairList'
                
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

def decode_obj_props(gd_type, gd_format, key):
    
    match gd_type:
        
        case 'int' | 'integer' | 'number':
            if (enum:=match_enum(gd_format)):
                return enum+'.from_string'
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
                
                case  'events':
                    return "EventList"
                
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
            return 'from_bool'
        
        case 'float' | 'real':
            return 'from_float'
        
        case 'str' | 'string':
            
            match gd_format:
                
                case 'base64':
                    return 'encode_text'
                
                case 'hsv':
                    return 'to_string'
                
                case 'particle':
                    return 'to_string'
                
                case 'groups' | 'parent_groups' | 'events':
                    return 'to_string'
                
                case  'weights' | 'sequence' | 'group weights' | 'group counts':
                    return 'to_string'
                
                case 'remaps' |'group remaps':
                    return 'to_string'
                    
                case 'colors':
                    return 'to_string'
                
                case 'guidelines':
                    return 'to_string'
                
                case 'color':
                    return 'to_string'
                
                case _:
                    return 'str'
        case _:
            return

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
            'decode': decode_obj_props(g['type'].iloc[0], g['format'].iloc[0], g.index[0]),
            'encode': encode_obj_props(g['type'].iloc[0], g['format'].iloc[0], g.index[0]),
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

if __name__ == "__main__":
    main()