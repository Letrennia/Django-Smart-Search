import json
import math
import re
import os

# k <1.2, 2>
# b = 0.75
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_document_word_count = os.path.join(BASE_DIR, "document_count_words.json")
input_keyword_document_count = os.path.join(BASE_DIR, "keyword_document_count.json")
input_methods_document_count = os.path.join(BASE_DIR, "methods_document_count.json")

input_keywords = os.path.join(BASE_DIR, "..", "wordlists_dir", "keywords.txt")
input_methods = os.path.join(BASE_DIR, "..", "wordlists_dir", "methods.txt")

with open(input_document_word_count, "r", encoding="utf-8") as file:
    document_word_count = json.load(file)

with open(input_keyword_document_count, "r", encoding="utf-8") as file:
    keyword_document_count = json.load(file)

with open(input_methods_document_count, "r", encoding="utf-8") as file:
    methods_document_count = json.load(file)

input_path = os.path.join(input_keywords)
with open(input_path, "r", encoding="utf-8") as file:
    magic_words_keywords= [line.strip().lower() for line in file]

input_path = os.path.join(input_methods)
with open(input_path, "r", encoding="utf-8") as file:
    magic_words_methods = [line.strip() for line in file]

N = len(document_word_count)
avgdl = sum(document_word_count.values()) / N

def TF(document, word, type, k = 1.2, b = 0.75):
    if type == "keyword":
        freq = keyword_document_count[word][document]
    elif type == "method":
        freq = methods_document_count[word][document]

    document_len = document_word_count[document]

    numerator = freq * (k + 1)
    denominator = freq + (k * (1 - b + (b * (document_len / avgdl))))

    return numerator / denominator

def IDF(word, type):
    if type == "keyword":
        n = len(keyword_document_count[word])
    elif type == "method":
        n = len(methods_document_count[word])

    numerator = N - n + 0.5
    denominator = n + 0.5

    return math.log((numerator / denominator) + 1)

def score(document, word, type):
    return TF(document, word, type=type) * IDF(word, type)

def query_score(query):
    query_words = re.findall(r"[A-Za-z0-9_.]+(?:\(\))?", query)
    BM25_score = {}

    for word in query_words:
        # print(word)
        word_lower = word.lower()
        if word_lower not in magic_words_keywords and word not in magic_words_methods:
            continue

        if word_lower in magic_words_keywords:
            document_list = keyword_document_count[word_lower]
            for document in document_list:
                BM25_score[document] = BM25_score.get(document , 0) + score(document, word_lower, 'keyword')

        if word in magic_words_methods:
            document_list = methods_document_count[word]
            for document in document_list:
                BM25_score[document] = BM25_score.get(document , 0) + score(document, word, 'method')

    return BM25_score

# scores = query_score("abs()")
#
# items = scores.items()
# sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
# top_10 = sorted_items[:10]
#
# for doc, score in top_10:
#     print(doc, score)