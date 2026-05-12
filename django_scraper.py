from bs4 import BeautifulSoup
import requests
import re

url = 'https://docs.djangoproject.com/sitemap-en.xml'
html_text = requests.get(url, verify=False).text

soup = BeautifulSoup(html_text, 'lxml')

all_urls = []
pattern = r"/releases/\d+(\.\d+)*/?$"

for item in soup.find_all('loc'):
    if not re.search(pattern, item.text.strip()):
        all_urls.append(item.text)



num = 1
for url in all_urls:
    django_text = requests.get(url, verify=False).text
    django_soup = BeautifulSoup(django_text, 'lxml')

    for tag in django_soup(['nav', 'footer', 'head', 'header']):
        tag.decompose()

    for tag in django_soup.find_all('div', {'role': 'complementary'}):
        tag.decompose()

    for tag in django_soup.find_all('div', class_=['doc-floating-warning', 'skip-link', 'container container--flex container--flex--wrap--mobile',
                                                   'highlight-default notranslate', 'highlight-apache notranslate', 'highlight-pycon notranslate',
                                                   'highlight-console notranslate', 'highlight-text notranslate', 'code-block-caption',
                                                   'highlight-python notranslate', 'highlight-html+django notranslate',
                                                   'highlight-javascript notranslate', 'highlight-html+jinja notranslate',
                                                   'last highlight-default notranslate']):
        tag.decompose()

    for tag in django_soup.find_all('div', id=['billboard', 'version-switcher']):
        tag.decompose()

    for tag in django_soup.find_all('a', class_=['skip-link', 'backtotop']):
        tag.decompose()

    for tag in django_soup.find_all('aside', class_=['footnote-list brackets']):
        tag.decompose()

    for tag in django_soup.find_all('p', class_=['rubric']):
        tag.decompose()




    # text = django_soup
    text = django_soup.get_text()

    with open(f'data_dir/file_{num}.txt', 'a', encoding='utf-8') as f:
        f.write(url + '\n')
        f.write(text + '\n')
        f.write(text)

    num+=1


    # print(text)
    # print(url)



