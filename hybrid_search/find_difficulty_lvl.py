import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

input_file = os.path.join(BASE_DIR, "wordlists_dir", "weights_dir", "file_level.txt")

def find_difficulty(file):
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            file_name, lvl = line.split()

            if file_name == file:
                return lvl


# TEST
# dif = find_difficulty('file_30.txt')
# print(dif)