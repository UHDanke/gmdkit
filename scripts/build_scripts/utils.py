from collections import defaultdict
from pathlib import Path
import os
import shutil
import re

def tree():
    return defaultdict(tree)


def build_tree(root, aliases):

    for path, val in aliases.items():
        parts = path.split('.')
        node = root
        for part in parts[:-1]:
            node = node[part]
        node[parts[-1]] = val

def clear_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)

def render_tree(node, base_path) -> None:
    base_path = Path(base_path)
    base_path.mkdir(parents=True, exist_ok=True)

    val_keys = [k for k, v in node.items() if not isinstance(v, dict)]
    dict_keys = [k for k, v in node.items() if isinstance(v, dict)]

    init_lines = []
    for key in val_keys:
        val = node[key]
        init_lines.append(f"{key} = {repr(val)}")

    for key in dict_keys:
        init_lines.append(f"from . import {key}")

    (base_path / "__init__.py").write_text("\n".join(init_lines) + "\n")

    for key in dict_keys:
        render_tree(node[key], base_path / key)

def sort_number(s:int|str) -> str | None:
    if isinstance(s, int):
        return 0, "", s
    elif isinstance(s, str):
        match = re.search(r"^(.*?)(\d+)$", s.strip())
        if match:
            return 1, match.group(1), int(match.group(2))
        else:
            return 2, s, 0
    
    return 0, "", s