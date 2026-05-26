import os
import re
import json

input_dir = "../clean_data"
input_keywords = "../wordlists_dir/keywords.txt"
input_methods = "../wordlists_dir/methods.txt"


magic_word_dictionary = {}

# Wyrazy z pliku keywords
input_path = os.path.join(input_keywords)
with open(input_path, "r", encoding="utf-8") as file:
    magic_words = [line.strip().lower() for line in file]


for filename in os.listdir(input_dir):
    input_path = os.path.join(input_dir, filename)

    with open(input_path, "r", encoding="utf-8") as file:
        content = file.read()

    if "[TEXT]" in content:
        text = content.split("[TEXT]")[1].split("[VECTOR]")[0].strip()
        words = re.findall(r"[A-Za-z0-9_.]+", text.lower())

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

with open("keyword_document_count.json", "w", encoding="utf-8") as file:
    json.dump(sorted_dict, file, ensure_ascii=False, indent=4)

# for word, articles in magic_word_dictionary.items():
#     print(word)
#     for article, count in articles.items():
#         print(" ", article, ": ", count)


with open("keyword_document_count.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print(len(data))
