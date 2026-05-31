import os
import re
import shutil

input_dir = "../clean_data"
output_dir = "../no_duplicate_data"

seen = {}
original_files = []
duplicate_files = []

for filename in os.listdir(input_dir):
    path = os.path.join(input_dir, filename)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"\[TEXT\](.*)", content, re.DOTALL)
    normalized = re.sub(r"[^a-zA-Z0-9]","", match.group(1).lower())

    if normalized not in seen:
        seen[normalized] = filename
        original_files.append(filename)
        source = path
        destination = os.path.join(output_dir, filename)
        shutil.copyfile(source, destination)
    else:
        duplicate_files.append(filename)

print(len(original_files))
print(len(duplicate_files))
#
# with open("duplicates.txt", "w", encoding="utf-8") as file:
#     for filename in duplicate_files:
#         file.write(filename + "\n")