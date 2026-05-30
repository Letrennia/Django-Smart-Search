import os
from urllib.parse import urlparse
import json

input_dir = "../clean_data"
tree = {}

for filename in os.listdir(input_dir):
    input_path = os.path.join(input_dir, filename)

    with open(input_path, "r", encoding="utf-8") as file:
        content = file.read()

    if "[URL]" in content:
        url = content.split("[URL]")[1].split("[TEXT]")[0].strip()
        parsed = urlparse(url)
        path_parts = [p for p in parsed.path.split("/") if p]

        if path_parts and path_parts[0] == "en":
            path_parts = path_parts[1:]

        new_tree = tree

        for part in path_parts:
            if part not in new_tree:
                new_tree[part] = {}
            new_tree = new_tree[part]

with open("url_tree.json", "w", encoding="utf-8") as file:
    json.dump(tree, file, indent=4)
