import os
import re

import ftfy # fixes text for you <3
import spacy
import json

input_dir = "../data_dir"
output_dir = "../clean_data"
comper_dir = "../duplicates.txt"

with open(comper_dir, "r", encoding="utf-8") as file:
    duplicates = set(line.strip() for line in file)

os.makedirs(output_dir, exist_ok=True)

# nlp = spacy.load("en_core_web_sm")

all = set()
all_keywords = set()
all_themes = set()
all_methods = set()

count_keywords = {}
count_themes = {}
all_sentences = []

all_t = 0
max_t = 0
min_t = 1000000

article_lenght = {}

for filename in os.listdir(input_dir):
    count_t = 0

    if filename in duplicates:
        continue

    input_path = os.path.join(input_dir, filename)

    with open(input_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Thatâ€™s it! -> That's it!
    clean = ftfy.fix_text(content)

    all.update(re.findall(r"([A-Za-z0-9_. ]+)¶", content))

    file_keywords = []
    file_themes = []

    for thing in all:
        thing = thing.strip()
        if len(thing.split()) == 1:
            all_keywords.add(thing)
            file_keywords.append(thing)
        else:
            all_themes.add(thing)
            file_themes.append(thing)

    count_keywords[filename] = len(file_keywords)
    count_themes[filename] = len(file_themes)

    all_methods.update(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\(\)", content))

    # ¶ -> u00b6
    clean = clean.replace("\u00b6", " ")

    # Znaczki/Logo windowsa, linuxa i maca
    clean = clean.replace("/", " ")
    clean = clean.replace("", " ")
    clean = clean.replace("", " ")

    # Usunięcie luźnych zdań pozostałych po usunięciu kodu
    clean = clean.replace("For example:", "")
    clean = clean.replace("Usage example:", "")
    clean = clean.replace("Example usage:", "")
    clean = clean.replace("This example would return this HTML:", "")
    clean = clean.replace("Here's a typical usage example:", "")

    # Terminal
    clean = re.sub(r"\.\.\.\\>", "", clean)

    # Usunięcie zbędnych enterów -> zmniejszenie pliku
    clean = re.sub(r"\n+", "\n", clean)

    # Kod
    clean = re.sub(r"^>>>.*(?:\n|$)", "", clean, flags=re.MULTILINE)
    clean = re.sub(r"function\s+\w*\s*\([^)]*\)\s*\{[\s\S]*?\}", "", clean)
    clean = re.sub(r"const\s+\w+\s*=\s*[\s\S]*?(;|\n\s*\n)", "", clean)
    clean = re.sub(r"fetch\([\s\S]*?\)\.then\([\s\S]*?\}\);?", "", clean)

    # html
    clean = re.sub(r"<p[\s\S]*?</p>", "", clean)
    # clean = re.sub(r"<style[\s\S]*?</style>", "", clean)
    # clean = re.sub(r"<script[\s\S]*?</script>", "", clean)

    # Bardzo długie
    # doc = nlp(clean)
    # # Wyrazy - tokeny
    # for token in doc:
    #     if token.is_space or token.is_punct:
    #         continue
    #     count_t += 1
    #     all_t += 1
    #     # print(token)

    count_t = len(re.findall(r"\b[\w_]+\b", clean))
    article_lenght[filename] = count_t

    all_t += count_t

    max_t = count_t if max_t < count_t else max_t
    min_t = count_t if min_t > count_t else min_t

    # Zdania
    sentences = re.findall(r"[^.!?]+[.!?](?=\s|$)", clean.strip())
    all_sentences.extend(sentences)

    # output_path = os.path.join(output_dir, filename)

    # # Nagłowki
    # file_id = filename.replace("file_", "").replace(".txt", "")
    # lines = clean.splitlines()
    # url = ""
    # text_start = 0
    #
    # if lines and lines[0].startswith("https"):
    #     url = lines[0].strip()
    #     text_start = 1
    #
    # text = "\n".join(lines[text_start:]).strip()
    #
    # final_output = (
    #     f"[ID]\n"
    #     f"{file_id}\n"
    #     f"[URL]\n"
    #     f"{url}\n"
    #     f"[TEXT]\n"
    #     f"{text}\n"
    #     f"[VECTOR]\n"
    # )
    # with open(output_path, "w", encoding="utf-8") as file:
    #     file.write(final_output)

all_methods = sorted(all_methods)
all_keywords = sorted(all_keywords)
all_themes = sorted(all_themes)

print("Minimum keywords: ", min(count_keywords.values()))
print("Minimum themes: ", min(count_themes.values()))

print("Maximum keywords: ", max(count_keywords.values()))
print("Maximum themes: ", max(count_themes.values()))

print("Avg keywords:", sum(count_keywords.values()) / len(count_keywords.values()))
print("Avg themes:", sum(count_themes.values()) / len(count_themes.values()))

# with open("../wordlists_dir/keywords.txt", "w", encoding="utf-8") as file:
#     file.write("\n".join(all_keywords))
#
# with open("../wordlists_dir/themes.txt", "w", encoding="utf-8") as file:
#     file.write("\n".join(all_themes))
#
# with open("../wordlists_dir/methods.txt", "w", encoding="utf-8") as file:
#     file.write("\n".join(all_methods))

sorted_article_lenght = dict(sorted(article_lenght.items()))

# with open("../BM25/document_count_words.json", "w", encoding="utf-8") as file:
#     json.dump(sorted_article_lenght, file, ensure_ascii=False, indent=4)

count_words = 0
mini = 60000
maks = 0

for sentence in all_sentences:
    words = re.findall(r"[A-Za-z_][A-Za-z0-9_\.]*\(?\)?", sentence)

    if (len(words)) == 0:
        continue

    mini = min(mini, len(words))
    maks = max(maks, len(words))
    count_words += len(words)
    # if(len(words) == 1):
    #     print(sentence)

print("Minimalna ilość słów w zdaniu:", mini)
print("Maksumalna ilość słów w zdaniu:", maks)
print("Avg słów w zdaniu: ", count_words / len(all_sentences))
print(count_words)

print("Najmniejsza ilość słów w artykule: ", min_t)
print("Największa ilość słów w artykule: ", max_t)
print("Średnia ilość słów w artykule: ", round((all_t // 6031), 2))

# print(all_keywords)
# print(all_methods)
