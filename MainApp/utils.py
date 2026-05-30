import re

def parse_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    url_match = re.search(r"\[URL\]\s*(.+)", content)
    url = url_match.group(1).strip()

    text_match = re.search(r"\[TEXT\]\s*(.+)", content)
    title = text_match.group(1).strip()

    return title, url