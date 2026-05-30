import os
import re
import json

input_dir = "../clean_data"
input_methods = "../wordlists_dir/methods.txt"

method_map = {}
with open(input_methods, "r", encoding="utf-8") as f:
    for line in f:
        raw = line.rstrip("\n")
        if not raw.strip():
            continue
        raw_stripped = raw.strip().lstrip("\ufeff")
        original = raw_stripped
        normalized = re.sub(r"\(\)\s*$", "", raw_stripped)
        if normalized not in method_map:
            method_map[normalized] = original

magic_words = set(method_map.keys())

magic_word_dictionary = {}
pattern = re.compile(r"([\w.]+)\s*\(")

for filename in os.listdir(input_dir):
    path = os.path.join(input_dir, filename)
    if not os.path.isfile(path):
        continue
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    if "[TEXT]" in content:
        text = content.split("[TEXT]")[1].split("[VECTOR]")[0].strip()

        found = pattern.findall(text)
        found = [w.split(".")[-1] for w in found]

        for word in found:
            word_norm = word.rstrip("()")
            if word_norm in magic_words:
                magic_word_dictionary.setdefault(word_norm, {}).setdefault(filename, 0)
                magic_word_dictionary[word_norm][filename] += 1

sorted_dict = {}
for norm in sorted(magic_word_dictionary.keys()):
    orig = method_map.get(norm, norm + "()")
    sorted_dict[orig] = {d: magic_word_dictionary[norm][d] for d in sorted(magic_word_dictionary[norm])}

with open("../BM25/methods_document_count.json", "w", encoding="utf-8") as file:
    json.dump(sorted_dict, file, ensure_ascii=False, indent=4)

print(len(sorted_dict))