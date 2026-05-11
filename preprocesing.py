import ftfy # fixes text for you <3
import re

with open("data_dir/file_667.txt", "r", encoding="utf-8") as file:
    content = file.read()
    # print(content)

# Thatâ€™s it! -> That's it!
clean = ftfy.fix_text(content)

# Techniczne specjalne słowa
keywords = list(dict.fromkeys(re.findall(r"([A-Za-z0-9_. ]+)¶", content)))
print(keywords)
# Metody, funkjce
methods = list(dict.fromkeys(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\(\)", content)))
print(methods)

# ¶ -> u00b6
clean = clean.replace("\u00b6", " ")

# print(hex(ord("")))
# print(hex(ord("")))

# Tak nie działa, trzeba ręcznie
#  -> u29c4, 0xf17a
#  -> 0xf179
clean = clean.replace("/", " ")
clean = clean.replace("", " ")
clean = clean.replace("", " ")
clean = clean.replace("For example:", "")
clean = clean.replace("Usage examples:", "")

clean = re.sub(r"\.\.\.\\>", "", clean)
# clean = re.sub(r"(?<!\n)\n(?!\n)", " ", clean)
clean = re.sub(r"\n+", "\n", clean)

# Kod
clean = re.sub(r"^>>>.*(?:\n|$)", "", clean, flags=re.MULTILINE)
clean = re.sub(r"function\s+\w*\s*\([^)]*\)\s*\{[\s\S]*?\}", "", clean)
clean = re.sub(r"const\s+\w+\s*=\s*[\s\S]*?(;|\n\s*\n)", "", clean)
clean = re.sub(r"fetch\([\s\S]*?\)\.then\([\s\S]*?\}\);?","",clean)

# html
# clean = re.sub(r"<form[\s\S]*?</form>", "", clean)
# clean = re.sub(r"<style[\s\S]*?</style>", "", clean)
# clean = re.sub(r"<script[\s\S]*?</script>", "", clean)

print(clean)