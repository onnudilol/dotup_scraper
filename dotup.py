import re
import requests
from bs4 import BeautifulSoup
import configparser


config = configparser.ConfigParser()
config.read('settings.ini')

links = []
files = []
oldest_id = config['Files']['oldest_id']

counter = 2
page = str(counter) + '.html'

# This regular expression returns the file IDs
id_re = re.compile(r'org([0-9]+.[a-z0-9]{3})')


def get_links(link_list):
    for link in link_list.find_all('a', href=True):
        links.append(link['href'])


def get_page(page_number=''):
    req = requests.get('http://www.dotup.org/' + page_number)
    content = req.content
    soop = BeautifulSoup(content, "lxml")
    return soop


def filter_links(unsorted):
    for i in unsorted:
        if id_re.search(i):
            files.append(id_re.search(i).group(1))


def crawler(count=''):
    h = get_page(count)
    get_links(h)
    filter_links(links)


if __name__ == "__main__":
    crawler()

    while oldest_id not in files:
        crawler(page)
        counter += 1
        page = str(counter) + '.html'

    id_index = files.index(oldest_id)
    files = files[:id_index]

    config['Files']['oldest_id'] = files[0]

    with open('settings.ini', 'w') as settings:
        config.write(settings)

    with open('url_list.txt', 'w') as urls:
        for f in files:
            urls.write('http://www.dotup.org/uploda/www.dotup.org' + f + '\n')
