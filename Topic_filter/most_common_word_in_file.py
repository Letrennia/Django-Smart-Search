import json
from collections import defaultdict

with open("../BM25/keyword_document_count.json", "r", encoding="utf-8") as file:
    data = json.load(file)

file_dict = defaultdict(dict)
stopwords = {"a", "in", "if", "s", "for", "with"}

for keyword, files in data.items():
    if keyword in stopwords:
        continue

    for file_name, count in files.items():
        file_dict[file_name][keyword] = count
result = {}

for file_name, kw_dict in file_dict.items():
    sorted_kw = sorted(kw_dict.items(), key=lambda x: x[1], reverse=True)
    top3 = [kw for kw, count in sorted_kw[:3]]
    result[file_name] = top3


with open(".most_common_3_for_file.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)