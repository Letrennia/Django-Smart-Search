import json

with open("../wordlists_dir/keywords.txt", "r", encoding="utf-8") as file:
    all_keywords = set(line.strip().lower() for line in file)

with open("../BM25_data/keyword_document_count.json", "r", encoding="utf-8") as file:
    data = json.load(file)

found_keywords = set(data.keys())

missing_keywords = sorted(all_keywords - found_keywords)

existing_keywords = sorted(found_keywords)

print("Liczba wszystkich keywords:", len(all_keywords))
print("Liczba znalezionych keywords:", len(found_keywords))
print("Liczba brakujących keywords:", len(missing_keywords))

print("Brakujące:")

for word in missing_keywords:
    print(word)

for word in existing_keywords:
    print(word)

coverage = len(found_keywords) / len(all_keywords) * 100

print(f"\nPokrycie keywords: {coverage:.2f}%")