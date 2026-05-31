# suma wag keyword lub method

import os

import spacy


def read_weights(filename):
    items_pair = {}
    with open(filename, 'r', encoding='utf-8') as f_w:
        for line in f_w:
            a, b = line.split()
            items_pair[a] = float(b)

    return items_pair


def read_content(filename):
    with open(filename, 'r', encoding='utf-8') as f_c:
        file_content = f_c.read()
        start = file_content.find('[TEXT]')
        end = file_content.find('[VECTOR]')

        text_content = file_content[start + 6:end].strip()

    return text_content


def calculate_weights(item_pair, text_content):
    item_sum = 0
    for word in text_content.split():
        if word in item_pair:
            item_sum += item_pair[word]

    return item_sum


def calculate_avg_sentences_len(text_content):
    all_words = 0
    sentences_count = 0
    doc = nlp(text_content)
    for sent in doc.sents:
        all_words += len(sent.text.split())
        sentences_count += 1

    return all_words / sentences_count



nlp = spacy.load('en_core_web_sm')
keywords_pair = read_weights('../wordlists_dir/weights_dir/keywords_weights.txt')
methods_pair = read_weights('../wordlists_dir/weights_dir/methods_weights.txt')


input_dir = "../no_duplicate_data"

for file in os.listdir(input_dir):
    if not file.endswith(".txt"):
        continue

    input_path = os.path.join(input_dir, file)

    content = read_content(input_path)

    # KEYWORDS METHODS SUM
    keywords_sum = calculate_weights(keywords_pair, content)
    methods_sum = calculate_weights(methods_pair, content)
    final_sum = keywords_sum * 0.3 + methods_sum
    with open('../wordlists_dir/weights_dir/file_weights_updated.txt', 'a') as f:
        f.write(f'{file} {final_sum}\n')

    # SENTENCES WRITE
    word_per_sentence = calculate_avg_sentences_len(content)
    with open('../wordlists_dir/weights_dir/file_words_sentences.txt', 'a') as f:
        f.write(f'{file} {word_per_sentence}\n')















# THEMES
# def read_weights_themes(filename):
#     items_pair = {}
#     with open(filename, 'r') as f:
#         for line in f:
#             a, b = line.rsplit(" ", 1)
#             items_pair[a] = float(b)
#
#     return items_pair


# def calculate_weights_themes(item_pair, text_content):
#     item_sum = 0
#     for phrase, weight in item_pair.items():
#         if phrase in text_content:
#             item_sum += weight
#             print(phrase, weight)
#
#     return item_sum