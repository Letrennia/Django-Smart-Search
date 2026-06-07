import json
from collections import defaultdict, Counter

file_to_cluster = {}

with open("file_clusters.txt", "r", encoding="utf-8") as f:
    for line in f:
        file, cluster = line.strip().split(";")
        file_to_cluster[file] = cluster

with open(".most_common_3_for_file.json", "r", encoding="utf-8") as f:
    file_to_keywords = json.load(f)

cluster_words = defaultdict(list)

for file, keywords in file_to_keywords.items():

    cluster = file_to_cluster.get(file)
    if cluster is None:
        continue

    cluster_words[cluster].extend(keywords)

cluster_sorted = {}

for cluster, words in cluster_words.items():
    counts = Counter(words)
    sorted_words = sorted(
        counts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    cluster_sorted[cluster] = sorted_words

with open("cluster_keywords.txt", "w", encoding="utf-8") as f:
    for cluster, words in cluster_sorted.items():
        f.write(f"{cluster}:\n")

        for word, count in words:
            f.write(f"{word}: {count}\n")

        f.write("\n")