import re
from collections import defaultdict

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


def render_tree(node, indent=0):
    lines = []
    indent_str = '    ' * indent
    
    
    val_keys = [k for k, v in node.items() if not isinstance(v, defaultdict)]
    dd_keys = [k for k, v in node.items() if isinstance(v, defaultdict)]
    
    def sort_key(k):
        v = node[k]
        if isinstance(v, int):
            return (0, v)
        if isinstance(v, str) and v.isdigit():
            return (0, int(v))
        return (1, str(v))
    
    
    for key in sorted(val_keys, key=sort_key):
        val = node[key]
        
        lines.append(f"{indent_str}{key} = {repr(val)}")

    for key in sorted(dd_keys):
        val = node[key]
        lines.append('')
        lines.append(f"{indent_str}class {key}:")
        children = render_tree(val, indent + 1)
        if children:
            lines.extend(children)
        else:
            lines.append(f"{indent_str}    pass")
            
    return lines


def dict_repr(d, keys):
    parts = []
    for k, v in d.items():
        if v is not None:
            key_str = repr(k)
            val_str = repr(v) if k in keys else str(v)
            parts.append(f"{key_str}: {val_str}")
    return "{" + ", ".join(parts) + "}"