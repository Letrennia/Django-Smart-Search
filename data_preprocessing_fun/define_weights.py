# ocenia trudność (wagę) keyword lub method
# zapis do pliku txt w formacie (keyword waga) lub (method waga)

from collections import Counter
import ast

def ranking(item, all_):
    weights = {}
    weight = 0
    for rank, (item, freq) in enumerate(item):
        percent = rank / all_

        if percent < 0.1:
            weight = 0.1
        elif percent < 0.3:
            weight = 0.3
        elif percent < 0.5:
            weight = 0.5
        elif percent < 0.7:
            weight = 0.7
        elif percent < 0.9:
            weight = 0.8
        else:
            weight = 1.0

        weights[item] = weight

    return weights

def read_words(filename):
    with open(filename, 'r') as f:
        file_words = [line.strip() for line in f if line.strip()]

    return file_words

def read_methods(filename):
    count_ = Counter()
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()

            item_list = ast.literal_eval(line)

            count_.update(item_list)

    return count_


def write_into_file(filepath, phrases):
    with open(filepath, 'w') as f:
        for phrase, weight in phrases.items():
            f.write(f'{phrase} {weight}\n')



# KEYWORDS

words = read_words('../wordlists_dir/weights_dir/keywords_duplicate.txt')
words_unique = read_words('../wordlists_dir/keywords.txt')

count_words = Counter(words)
sorted_words = count_words.most_common()
all_words = len(words_unique)

weights_key = ranking(sorted_words, all_words)
write_into_file('../wordlists_dir/weights_dir/keywords_weights.txt', weights_key)



# THEMES

# theme = read_words('../wordlists_dir/weights_dir/themes_duplicate.txt')
# theme_unique = read_words('../wordlists_dir/themes.txt')
#
# count_theme = Counter(theme)
# sorted_theme = count_theme.most_common()
# all_themes = len(theme_unique)
#
# weights_theme = ranking(sorted_theme, all_themes)
# write_into_file('../wordlists_dir/weights_dir/themes_weights.txt', weights_theme)



# METHODS


methods = read_methods('../wordlists_dir/weights_dir/methods_duplicate.txt')
methods_unique = read_words('../wordlists_dir/methods.txt')

count_methods = Counter(methods)
sorted_methods = count_methods.most_common()
all_methods = len(methods_unique)

weights_method = ranking(sorted_methods, all_methods)
write_into_file('../wordlists_dir/weights_dir/methods_weights.txt', weights_method)

