from collections import Counter
import ast

from matplotlib import pyplot as plt


def read_words(filename):
    with open(filename, 'r') as f:
        file_words = [line.strip() for line in f if line.strip()]

    return file_words

def read_methods(filename):
    count_ = Counter()
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()

            item_list = ast.literal_eval(line)

            count_.update(item_list)

    return count_


def plot_bar_chart(data, x_label, y_label, title):
    data = data[:50]
    labels = [x for x, _ in data]
    counts = [y for _, y in data]

    plt.bar(labels, counts)
    plt.yscale('log')
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.xticks(rotation=90)
    plt.show()


# KEYWORDS
keywords = read_words('../wordlists_dir/weights_dir/keywords_duplicate.txt')
count_keywords = Counter(keywords)
sorted_keywords = count_keywords.most_common()
plot_bar_chart(sorted_keywords, 'Keywords', 'Quantity', 'Top 50 keywords')

# METHODS
methods = read_methods('../wordlists_dir/weights_dir/methods_duplicate.txt')
count_methods = Counter(methods)
sorted_methods = count_methods.most_common()
plot_bar_chart(sorted_methods, 'Methods', 'Quantity', 'Top 50 methods')

