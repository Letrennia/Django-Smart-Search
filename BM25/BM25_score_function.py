import json
import math
import re
import os

# k <1.2, 2>
# b = 0.75

input_document_word_count = "document_count_words.json"
input_keyword_document_count = "keyword_document_count.json"
input_keywords = "../wordlists_dir/keywords.txt"

with open(input_document_word_count, "r", encoding="utf-8") as file:
    document_word_count = json.load(file)

with open(input_keyword_document_count, "r", encoding="utf-8") as file:
    keyword_document_count = json.load(file)

input_path = os.path.join(input_keywords)
with open(input_path, "r", encoding="utf-8") as file:
    magic_words = [line.strip().lower() for line in file]

N = len(document_word_count)
avgdl = sum(document_word_count.values()) / N

def TF(document, word, k = 1.2, b = 0.75):
    freq = keyword_document_count[word][document]
    document_len = document_word_count[document]

    numerator = freq * (k + 1)
    denominator = freq + (k * (1 - b + (b * (document_len / avgdl))))

    return numerator / denominator

def IDF(word):
    n = len(keyword_document_count[word])
    numerator = N - n + 0.5
    denominator = n + 0.5

    return math.log((numerator / denominator) + 1)

def score(document, word):
    return TF(document, word) * IDF(word)

def test(query = "How to make a view?"):
    query_words = re.findall(r"[A-Za-z0-9_.]+", query.lower())
    BM25_score = {}

    for word in query_words:
        if word not in magic_words:
            continue

        document_list = keyword_document_count[word]
        for document in document_list:
            BM25_score[document] = BM25_score.get(document , 0) + score(document, word)

    return BM25_score

scores = test("How to make a view?")

items = scores.items()
sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
top_10 = sorted_items[:10]

for doc, score in top_10:
    print(doc, score)