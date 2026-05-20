import os
import re

import ftfy # fixes text for you <3


input_dir = "../data_dir"

all_ = []
all_keywords = []
all_themes = []
all_methods = []


for filename in os.listdir(input_dir):

    if not filename.endswith(".txt"):
        continue

    input_path = os.path.join(input_dir, filename)

    with open(input_path, "r", encoding="utf-8") as file:
        content = file.read()

    clean = ftfy.fix_text(content)
    all_.extend(re.findall(r"([A-Za-z0-9_. ]+)¶", content))

    for thing in all_:
        thing = thing.strip()
        if len(thing.split()) == 1:
            all_keywords.append(thing)
        else:
            all_themes.append(thing)

    all_methods.append(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\(\)", content))

print(f' keywords: {len(all_keywords)}')
print(f'themes: {len(all_themes)}')
print(f'methods: {len(all_methods)}')



with open('../wordlists_dir/weights_dir/keywords_duplicate.txt', 'w') as file:
    for item in all_keywords:
        file.write(str(item) + '\n')

with open('../wordlists_dir/weights_dir/themes_duplicate.txt', 'w') as file:
    for item in all_themes:
        file.write(str(item) + '\n')

with open('../wordlists_dir/weights_dir/methods_duplicate.txt', 'w') as file:
    for item in all_methods:
        file.write(str(item) + '\n')

