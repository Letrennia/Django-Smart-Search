from django.shortcuts import render
from django.conf import settings
from .utils import parse_file
import os
from hybrid_search.hybrid_search_fun import hybrid_search
from hybrid_search.find_difficulty_lvl import find_difficulty
import re

DOC_BASE_PATH = os.path.join(settings.BASE_DIR, "no_duplicate_data")
WORDLIST_PATH = os.path.join(settings.BASE_DIR, "wordlists_dir")
CHUNK_SIZE = 1950

CLUSTER_MAP = {}

with open(os.path.join(WORDLIST_PATH, "keywords.txt"), "r", encoding="utf-8") as f:
    keyword_list = [line.strip().lower() for line in f if line.strip()]

with open(os.path.join(WORDLIST_PATH, "methods.txt"), "r", encoding="utf-8") as f:
    methods_list = [line.strip() for line in f if line.strip()]

with open(os.path.join(settings.BASE_DIR, "Topic_filter", "file_clusters.txt"), "r", encoding="utf-8") as f:
    for line in f:
        file, cluster = line.strip().split(";")
        CLUSTER_MAP[file] = cluster


def home(request):
    query = request.GET.get('q', '')
    selected_clusters = request.GET.getlist("cluster")
    results = []

    if query:
        final_scores = hybrid_search(query)

        for doc, score, chunk in final_scores[:30]:
            cluster = CLUSTER_MAP[doc]

            if selected_clusters and cluster not in selected_clusters:
                continue

            file_path = os.path.join(DOC_BASE_PATH, doc)
            title, url = parse_file(file_path)
            difficulty_lvl = find_difficulty(doc)
            text_excerpt = text_part(file_path, query, chunk)

            results.append({"title": title,
                            "url": url,
                            "file": doc,
                            "score": score,
                            "difficulty": difficulty_lvl,
                            "text_excerpt": text_excerpt})

    return render(request, "home.html", {"query": query, "results": results, "selected_clusters": selected_clusters})

def text_part(file_path, query, chunk):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    text = text.split("[TEXT]")[1].split("[VECTOR]")[0]
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if len(lines) > 1:
        lines = lines[1:]

    text = " ".join(lines)

    query_lower = set(query.lower().split())
    query = set(query.split())

    matched_keywords = [k for k in keyword_list if k in query_lower]
    matched_methods = [m for m in methods_list if m in query]
    words = text.split()

    # print(file_path, (matched_keywords), len(matched_methods))

    if not matched_keywords and not matched_methods:
        chunk = int(chunk)
        start = (chunk - 1) * CHUNK_SIZE
        end = start + 64
        snippet_words = words[start:end]
        snippet = " ".join(snippet_words)

        return "..." + snippet + "..."

    for i, word in enumerate(words):
        word_clean_lower = word.lower().strip(".,!?;:")
        word_clean = word.strip(".,!?;:")

        if word_clean_lower in matched_keywords or word_clean in matched_methods:
            start = max(0, i - 32)
            end = min(len(words), i + 32)

            snippet_words = words[start:end]
            snippet_words[i - start] = f"<span class='highlight'>{words[i]}</span>"
            snippet = " ".join(snippet_words)

            if end < len(words):
                snippet += "..."

            return snippet

    return ""