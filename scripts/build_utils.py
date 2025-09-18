import re
from collections import defaultdict
from pathlib import Path

# idk why it doesnt work
def sort_id(s):
    if str(s).isdigit():
        return (0, '', int(s))
    m = re.match(r"([^\d]+)(\d+)$", str(s))
    if m:
        prefix, num = m.group(1), int(m.group(2))
        print(prefix,num)
        return (1, prefix, num)
    return (2, str(s), -1)


class LineWriter:
    
    def __init__(self, path):
        self.path = path
        self.open()
    def open(self):
        self.file = open(self.path,"w")        
        
    def close(self):
        self.file.close()
        
    def write(self, *lines):
        for line in lines:
            self.file.write(line+'\n')


def tree():
    return defaultdict(tree)


def build_tree(root, aliases):

    for path, val in aliases.items():
        parts = path.split('.')
        node = root
        for part in parts[:-1]:
            node = node[part]
        node[parts[-1]] = val


def render_tree(node, base_path) -> None:
    base_path = Path(base_path)
    base_path.mkdir(parents=True, exist_ok=True)

    # Separate leaves (values) and nested modules
    val_keys = [k for k, v in node.items() if not isinstance(v, dict)]
    dict_keys = [k for k, v in node.items() if isinstance(v, dict)]

    # Write __init__.py
    init_lines = []
    for key in val_keys:
        val = node[key]
        init_lines.append(f"{key} = {repr(val)}")

    for key in dict_keys:
        init_lines.append(f"from . import {key}")

    (base_path / "__init__.py").write_text("\n".join(init_lines) + "\n")

    # Recursively write submodules
    for key in dict_keys:
        render_tree(node[key], base_path / key)


def dict_repr(d, keys):
    parts = []
    for k, v in d.items():
        if v is not None:
            key_str = repr(k)
            val_str = repr(v) if k in keys else str(v)
            parts.append(f"{key_str}: {val_str}")
    return "{" + ", ".join(parts) + "}"