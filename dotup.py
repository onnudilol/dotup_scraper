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


def get_page(page_number=''):
    req = requests.get('http://www.dotup.org/' + page_number)
    content = req.content
    soop = BeautifulSoup(content, "lxml")
    return soop


def get_links(link_list, unsorted_links):
    for link in link_list.find_all('a', href=True):
        unsorted_links.append(link['href'])


def filter_links(unsorted_list, sorted_list):
    for i in unsorted_list:
        if id_re.search(i):
            sorted_list.append(id_re.search(i).group(1))
    unsorted_list[:] = []


def output_url(output_file, input_list):
    with open(output_file, 'a') as url_list:
        for i in input_list:
            url_list.write('http://www.dotup.org/uploda/www.dotup.org' + i + '\n')


def crawler(count=''):
    h = get_page(count)
    get_links(h, links)
    filter_links(links, files)


if __name__ == "__main__":

    open('url_list.txt', w).close()
    crawler()
    output_url('url_list.txt', files)

    while oldest_id not in files:
        files = []
        crawler(page)
        output_url('url_list.txt', files)
        counter += 1
        page = str(counter) + '.html'

    else:
        id_index = files.index(oldest_id)
        files = files[:id_index]
        print(files)
        output_url('url_list.txt', files)

    config['Files']['oldest_id'] = files[0]

    with open('settings.ini', 'w') as settings:
        config.write(settings)
