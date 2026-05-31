from django.shortcuts import render
from django.conf import settings
from .utils import parse_file
import os

from BM25.BM25_score_function import query_score

DOC_BASE_PATH = os.path.join(settings.BASE_DIR, "clean_data")

def home(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        scores = query_score(query)
        not_dublicate = set()

        for doc, score in scores.items():
            file_path = os.path.join(DOC_BASE_PATH, doc)
            title, url = parse_file(file_path)
            #
            # title_score = (title, round(score,2))
            # if title_score in not_dublicate:
            #     continue
            # not_dublicate.add(title_score)

            results.append({"title": title,
                            "url": url,
                            "file": doc,
                            "score": score})

        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:50]

    return render(request, "home.html", {"query": query, "results": results})

