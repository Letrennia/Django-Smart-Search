import json

with open("document_count_words.json", "r") as file:
    document_count_words = json.load(file)

count = 0
for word_count in document_count_words.values():
    if word_count > 8192:
        count += 1

print(count)
print(len(document_count_words))
print(count/len(document_count_words) * 100)
