from gmdkit.serialization.functions import compress_string, decompress_string
from gmdkit.serialization.type_cast import encode_text, to_numkey
from gmdkit import Level
from gmdkit.defaults.objects import OBJECT_DEFAULT
from collections import defaultdict

key_range = range(2,700)

obj_id_range = OBJECT_DEFAULT.keys()
skip_range = {31}

start_key_formats = {
    "kA": range(1,100),
    "kS": range(1,100),
    "kI": range(1,100)
    }

value_default = "10.2.3.4"

value_override = {
    31: encode_text("TEST"),
    43: "0a1a1a0a0",
    44: "0a1a1a0a0",
    49: "0a1a1a0a0",
    57: "10.2.3.4.5.6",
    145: "30a-1a1a0.3a30a90a90a29a0a11a0a0a0a0a0a0a0a2a1a0a0a1a0a1a0a1a0a1a0a1a1a0a0a1a0a1a0a1a0a1a0a0a0a0a0a0a0a0a0a0a0a0a2a1a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0",
    152: "10.2.3.4.5.6",
    274: None,
    430: "10.2.3.4.5.6",
    435: "10.2.3.4.5.6",
    442: "10.2.3.4.5.6",
    "kA14": "1~2~3~4~5~6~",
    "kS29": "1_40_2_125_3_255_11_255_12_255_13_255_4_-1_6_1000_7_1_15_1_18_0_8_1",
    "kS30": "1_40_2_125_3_255_11_255_12_255_13_255_4_-1_6_1000_7_1_15_1_18_0_8_1",
    "kS31": "1_40_2_125_3_255_11_255_12_255_13_255_4_-1_6_1000_7_1_15_1_18_0_8_1",
    "kS32": "1_40_2_125_3_255_11_255_12_255_13_255_4_-1_6_1000_7_1_15_1_18_0_8_1",
    "kS33": "1_40_2_125_3_255_11_255_12_255_13_255_4_-1_6_1000_7_1_15_1_18_0_8_1",
    "kS34": "1_40_2_125_3_255_11_255_12_255_13_255_4_-1_6_1000_7_1_15_1_18_0_8_1",
    "kS35": "1_40_2_125_3_255_11_255_12_255_13_255_4_-1_6_1000_7_1_15_1_18_0_8_1",
    "kS36": "1_40_2_125_3_255_11_255_12_255_13_255_4_-1_6_1000_7_1_15_1_18_0_8_1",
    "kS37": "1_40_2_125_3_255_11_255_12_255_13_255_4_-1_6_1000_7_1_15_1_18_0_8_1",
    "kS38": "1_40_2_125_3_255_11_255_12_255_13_255_4_-1_6_1000_7_1_15_1_18_0_8_1|1_40_2_125_3_255_11_255_12_255_13_255_4_-1_6_1000_7_1_15_1_18_0_8_1|",    
    }


def create_keys():
    lvl = Level.default("Key Test",load_content=False)
    
    start_tokens = []
    
    for f, fr in start_key_formats.items():
        
        for i in fr:
            key = f"{f}{i}"
            
            if key in value_override:
                value = value_override[key]
            else:
                value = value_default
        
            if value is not None:
                start_tokens.append(str(key))
                start_tokens.append(value)
                
    start_string = ",".join(start_tokens) + ";"
    
    
    obj_list_tokens = []
    
    for k in obj_id_range:
        if k in skip_range:
            continue
        obj_tokens = ["1",str(k)]
        for key in key_range:
            if key in value_override:
                value = value_override[key]
            else:
                value = value_default
        
            if value is not None:
                obj_tokens.append(str(key))
                obj_tokens.append(value)
        
        obj_list_tokens.append(",".join(obj_tokens))
        
    obj_string = ";".join(obj_list_tokens) + ";"
    
    string = compress_string(start_string + obj_string)
    
    lvl['k4'].string = string
    
    lvl.to_file("data/gmd/offline")

def collapse_dict_of_sets(d: dict) -> dict[frozenset, set]:
    grouped = defaultdict(set)
    
    for key, value_set in d.items():
        grouped[frozenset(value_set)].add(key)
    
    return dict(grouped)

from typing import Dict, Set, Tuple, Any

def index_value_sets(
    d: Dict[Any, Set[Any]]
) -> Tuple[Dict[int, Set[Any]], Dict[int, Set[Any]]]:

    value_to_index: Dict[frozenset, int] = {}
    values_by_index: Dict[int, Set[Any]] = {}
    keys_by_index: Dict[int, Set[Any]] = {}

    next_index = 0

    for key, value_set in d.items():
        frozen = frozenset(value_set)

        idx = value_to_index.get(frozen)
        if idx is None:
            idx = next_index
            next_index += 1

            value_to_index[frozen] = idx
            values_by_index[idx] = set(value_set)  # store original mutable copy
            keys_by_index[idx] = {key}
        else:
            keys_by_index[idx].add(key)

    return values_by_index, keys_by_index

def test_keys():
    lvl = Level.from_file("data/gmd/offline/Key Test Output.gmd",load_content=False)
    
    key_collection = {}
    obj_collection = {}
    
    lvl_string = decompress_string(lvl['k4'].string)
    
    obj_tokens = lvl_string.removesuffix(";").split(";")
    
    for obj in obj_tokens:
    
        tokens = obj.split(",")
        it = iter(tokens)
        obj_dict = {}
        for k,v in zip(it,it):
            
            value_set = key_collection.setdefault(k, set())
            value_set.add(v)
            obj_dict[k] = v
    
        obj_id = obj_dict.get("1","")
        obj_keys = obj_collection.setdefault(obj_id,set())
        obj_keys.update(obj_dict.keys())
            
    
    return key_collection, obj_collection


key_collection, obj_collection = test_keys()
value_sets, grouped_objs = index_value_sets(obj_collection)