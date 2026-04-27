from gmdkit.serialization.functions import compress_string, decompress_string
from gmdkit.serialization.type_cast import encode_text, to_numkey
from typing import Dict, Set, Tuple, Any
import pandas as pd
from gmdkit import Level
from gmdkit.defaults.objects import OBJECT_DEFAULT
from collections import defaultdict

_key_range = range(2,700)

_obj_id_range = OBJECT_DEFAULT.keys()
_skip_range = {31}

_start_key_formats = {
    "kA": range(1,100),
    "kS": range(1,100),
    "kI": range(1,100)
    }

_value_default = "10.2.3.4"

_value_override = {
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

_quick_matches = {
    "1": "bool",
    "10": "int",
    "10.2": "float",
    "10.2.3.4.5.6": "string",
    "10.10.2.3.4.5.6": "string"
    
    }

_ignore_keys = {"1","155","156"}

def collapse_dict_of_sets(d: dict) -> dict[frozenset, set]:
    grouped = defaultdict(set)
    
    for key, value_set in d.items():
        grouped[frozenset(value_set)].add(key)
    
    return dict(grouped)

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
            values_by_index[idx] = set(value_set)
            keys_by_index[idx] = {key}
        else:
            keys_by_index[idx].add(key)

    return values_by_index, keys_by_index

def create_keys():
    lvl = Level.default("Key Test",load_content=False)
    
    start_tokens = []
    
    for f, fr in _start_key_formats.items():
        
        for i in fr:
            key = f"{f}{i}"
            
            if key in _value_override:
                value = _value_override[key]
            else:
                value = _value_default
        
            if value is not None:
                start_tokens.append(str(key))
                start_tokens.append(value)
                
    start_string = ",".join(start_tokens) + ";"
    
    
    obj_list_tokens = []
    
    for k in _obj_id_range:
        if k in _skip_range:
            continue
        obj_tokens = ["1",str(k)]
        for key in _key_range:
            if key in _value_override:
                value = _value_override[key]
            else:
                value = _value_default
        
            if value is not None:
                obj_tokens.append(str(key))
                obj_tokens.append(value)
        
        obj_list_tokens.append(",".join(obj_tokens))
        
    obj_string = ";".join(obj_list_tokens) + ";"
    
    string = compress_string(start_string + obj_string)
    
    lvl['k4'].string = string
    
    lvl.to_file("data/gmd/offline")



def test_keys():
    lvl = Level.from_file("data/gmd/offline/Key Test Output.gmd",load_content=False)
    
    key_collection = {}
    obj_collection = {}
    key_locations = {}
    
    lvl_string = decompress_string(lvl['k4'].string)
    
    obj_tokens = lvl_string.removesuffix(";").split(";")
    
    for obj in obj_tokens:
    
        tokens = obj.split(",")
        it = iter(tokens)
        obj_dict = {}
        for k,v in zip(it,it):
            obj_dict[k] = v
            
        obj_id = obj_dict.get("1","0")
        obj_keys = obj_collection.setdefault(obj_id,set())
        obj_keys.update(obj_dict.keys())
        
        
        for k,v in obj_dict.items():
            value_dict = key_collection.setdefault(k, {})
            value_set = value_dict.setdefault(v,set())
            value_set.add(obj_id)
            key_set = key_locations.setdefault(k,set())
            key_set.add(obj_id)
            if v not in _quick_matches.keys() and k not in _ignore_keys:
                print(obj_id,k,v)
            
    
    key_format = {}
    
    for k,v in key_collection.items():
        format_set = key_format.setdefault(k,set())
        
        for s in v:
            format_set.add(_quick_matches.get(s,"NA"))
            
    
    
    return key_collection, obj_collection, key_locations, key_format

def dot_join(values) -> str:
    if not values:
        return ""
    return ".".join(map(str, sorted(values)))


def export_key_collection(filepath: str, obj_collection: Dict[Any, Set[Any]]) -> None:
    df = pd.DataFrame.from_records(
        (
            {
                "key": key,
                "obj_values": dot_join(values),
            }
            for key, values in sorted(obj_collection.items())
        )
    )
    df.to_csv(filepath, index=False)


def export_obj_collection(filepath: str, obj_collection: Dict[Any, Set[Any]]) -> None:
    df = pd.DataFrame.from_records(
        (
            {
                "obj_key": key,
                "obj_values": dot_join(values),
            }
            for key, values in sorted(obj_collection.items())
        )
    )
    df.to_csv(filepath, index=False)


def export_value_sets(filepath: str, value_sets: Dict[int, Set[Any]]) -> None:
    df = pd.DataFrame.from_records(
        (
            {
                "value_index": idx,
                "value_set": dot_join(values),
            }
            for idx, values in sorted(value_sets.items())
        )
    )
    df.to_csv(filepath, index=False)


def export_grouped_objs(filepath: str, grouped_objs: Dict[int, Set[Any]]) -> None:
    df = pd.DataFrame.from_records(
        (
            {
                "value_index": idx,
                "grouped_objs": dot_join(keys),
            }
            for idx, keys in sorted(grouped_objs.items())
        )
    )
    df.to_csv(filepath, index=False)


def inclusion_graph_optimized(value_sets: Dict[int, Set[Any]]):
    subsets = {i: set() for i in value_sets}
    supersets = {i: set() for i in value_sets}

    items = sorted(value_sets.items(), key=lambda x: len(x[1]))

    for idx_i, set_i in items:
        for idx_j, set_j in items:
            if idx_i == idx_j:
                continue

            # prune by size
            if len(set_i) > len(set_j):
                continue

            if set_i.issubset(set_j):
                subsets[idx_i].add(idx_j)
                supersets[idx_j].add(idx_i)

    return subsets, supersets



key_collection, obj_collection, key_locations, key_format = test_keys()
value_sets, grouped_objs = index_value_sets(obj_collection)

key_collection, obj_collection, value_sets, grouped_objs
subsets, supersets = inclusion_graph_optimized(value_sets)
base_path = "data/txt/script_output"
export_key_collection(f"{base_path}/key_collection.csv", key_collection)
export_key_collection(f"{base_path}/key_format.csv", key_format)
export_obj_collection(f"{base_path}/obj_collection.csv", obj_collection)
export_value_sets(f"{base_path}/value_sets.csv", value_sets)
export_value_sets(f"{base_path}/subsets.csv", subsets)
export_value_sets(f"{base_path}/supersets.csv", supersets)
export_grouped_objs(f"{base_path}/grouped_objs.csv", grouped_objs)
