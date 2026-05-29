from matplotlib import pyplot as plt

def read_tuple_data(filename):
    items_tuple = {}
    with open(filename, 'r') as f_w:
        for line in f_w:
            a, b, c = line.split()
            items_tuple[a] = (float(b), float(c))

    return items_tuple


def read_weights(filename):
    items_pair = {}
    with open(filename, 'r', encoding='utf-8') as f_w:
        for line in f_w:
            a, b = line.split()
            items_pair[a] = float(b)

    return items_pair


def merge_files(file1, file2, file3):
    with open(file1, 'r') as f_1, open(file2, 'r') as f_2, open(file3, 'w') as f_3:
        for line1, line2 in zip(f_1, f_2):
            filename1, value1 = line1.strip().split()
            filename2, value2 = line2.strip().split()

            f_3.write(f'{filename1} {value1} {value2}\n')


def calculate_final_weight(items_tuple):
    for file, (value1, value2) in items_tuple.items():
        if value2 > 30 and value1 > 100:
            with open('../wordlists_dir/weights_dir/file_final_weights.txt', 'a') as f:
                f.write(f'{file} {0}\n')    #rozpiski
        elif value2 > 23:
            value_1_2 = value1 + 20 #dłuższe zdania
            with open('../wordlists_dir/weights_dir/file_final_weights.txt', 'a') as f:
                f.write(f'{file} {value_1_2}\n')
        else:
            with open('../wordlists_dir/weights_dir/file_final_weights.txt', 'a') as f:
                f.write(f'{file} {value1}\n')   #bez zmian


def plot_graph(value_data, x_label, y_label, bins_val=200):
    plt.figure(figsize=(10, 6), dpi=200)
    plt.hist(value_data, color='pink', bins=bins_val)
    # plt.yscale('log')
    plt.title(f'Rozkład wag ')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()

def weights_to_labels(data):
    for file, value in data.items():
        if value < 50:
            with open('../wordlists_dir/weights_dir/file_level.txt', 'a') as f:
                f.write(f'{file} EASY\n')
        elif value > 300:
            with open('../wordlists_dir/weights_dir/file_level.txt', 'a') as f:
                f.write(f'{file} HARD\n')
        else:
            with open('../wordlists_dir/weights_dir/file_level.txt', 'a') as f:
                f.write(f'{file} ADVANCED\n')




# merge_files(
#     '../wordlists_dir/weights_dir/file_weights_updated.txt',
#     '../wordlists_dir/weights_dir/file_words_sentences.txt',
#     '../wordlists_dir/weights_dir/merged_weights_sentences.txt'
# )



# tuple_data = read_tuple_data('../wordlists_dir/weights_dir/merged_weights_sentences.txt')
# calculate_final_weight(tuple_data)


pair_data = read_weights('../wordlists_dir/weights_dir/file_final_weights.txt')

# PLOT
# weights = list(pair_data.values())
# plot_graph(weights, 'Waga', 'Ilość artykułów')

weights_to_labels(pair_data)