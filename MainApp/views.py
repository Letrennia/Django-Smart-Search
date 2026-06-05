from django.shortcuts import render
from django.conf import settings
from .utils import parse_file
import os
from hybrid_search.hybrid_search_fun import hybrid_search
from hybrid_search.find_difficulty_lvl import find_difficulty

DOC_BASE_PATH = os.path.join(settings.BASE_DIR, "no_duplicate_data")

def home(request):
    query = request.GET.get('q', '')

    results = []

    if query:
        final_scores = hybrid_search(query)

        for doc, score in final_scores[:30]:
            file_path = os.path.join(DOC_BASE_PATH, doc)
            title, url = parse_file(file_path)

            difficulty_lvl = find_difficulty(doc)
            results.append({"title": title,
                            "url": url,
                            "file": doc,
                            "score": score,
                            "difficulty": difficulty_lvl})


    return render(request, "home.html", {"query": query, "results": results})

