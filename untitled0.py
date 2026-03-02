import re

with open("input.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Match "k" followed by anything except a quote
matches = re.findall(r'"k[^"]+"', text)

# Remove quotes
keys = [m.strip('"') for m in matches]

# Optional: remove duplicates while preserving order
seen = set()
unique_keys = []
for k in keys:
    if k not in seen:
        seen.add(k)
        unique_keys.append(k)

for key in unique_keys:
    print(key)