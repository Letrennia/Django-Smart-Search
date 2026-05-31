import os
import re
import json

input_dir = "../no_duplicate_data"
input_keywords = "../wordlists_dir/keywords.txt"
input_methods = "../wordlists_dir/methods.txt"

# def norm(w):
#     return w.strip().lower()

magic_word_dictionary = {}

# Wyrazy z pliku keywords
input_path = os.path.join(input_keywords)
with open(input_path, "r", encoding="utf-8") as file:
    magic_words = [line.strip() for line in file]


for filename in os.listdir(input_dir):
    input_path = os.path.join(input_dir, filename)

    with open(input_path, "r", encoding="utf-8") as file:
        content = file.read()

    if "[TEXT]" in content:
        text = content.split("[TEXT]")[1].split("[VECTOR]")[0].strip()
        # keywords
        words = re.findall(r"[A-Za-z0-9_.]+", text)
        # # methods
        # words = re.findall(r"[\w.]+\(\)", text.lower())
        # words = [word.split(".")[-1] for word in words]

        for word in words:
            if word in magic_words:
                if word not in magic_word_dictionary:
                    magic_word_dictionary[word] = {}
                if filename not in magic_word_dictionary[word]:
                    magic_word_dictionary[word][filename] = 0

                magic_word_dictionary[word][filename] += 1

sorted_dict = {}

for word in sorted(magic_word_dictionary.keys()):
    sorted_dict[word] = {}
    for doc in sorted(magic_word_dictionary[word].keys()):
        sorted_dict[word][doc] = magic_word_dictionary[word][doc]

with open("../BM25/keyword_document_count.json", "w", encoding="utf-8") as file:
    json.dump(sorted_dict, file, ensure_ascii=False, indent=4)

print(len(sorted_dict.items()))

# for word, articles in magic_word_dictionary.items():
#     print(word)
#     for article, count in articles.items():
#         print(" ", article, ": ", count)

# with open("../BM25/keyword_document_count.json", "r", encoding="utf-8") as file:
#     data = json.load(file)
#
# print(len(data))
