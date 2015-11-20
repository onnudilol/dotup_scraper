import re
import requests
from bs4 import BeautifulSoup
import configparser


config = configparser.ConfigParser()
config.read('settings.ini')

links = []
files = []
oldest_id = config['Files']['oldest_id']

# This regular expression returns the file IDs
id_url = re.compile(r'org([0-9]+.[a-z0-9]{1,4})')
id_num = re.compile(r'([0-9]+).[a-z0-9]{1,4}')


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
        if id_url.search(i):
            sorted_list.append(id_url.search(i).group(1))
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

    counter = 2
    page = str(counter) + '.html'

    open('url_list.txt', 'w').close()

    crawler()

    if oldest_id in files:
        id_index = files.index(oldest_id)
        final = files[:id_index]
        output_url('url_list.txt', final)
    else:
        output_url('url_list.txt', files)

    while oldest_id not in files:
        files = []
        crawler(page)

        if oldest_id in files:
            id_index = files.index(oldest_id)
            final = files[:id_index]
            output_url('url_list.txt', final)
            break

        else:

            if int(id_num.search(files[-1]).group(1)) < int(id_num.search(oldest_id).group(1)):
                files = [x.group(0) for f in files for x in [id_num.search(f)]
                         if int(x.group(1)) > int(id_num.search(oldest_id).group(1))]
                output_url('url_list.txt', files)
                break

            elif counter != 309:
                output_url('url_list.txt', files)
                counter += 1
                page = str(counter) + '.html'

            else:
                break

    with open('url_list.txt', 'r') as url_list:
        first = url_list.readline()
        config['Files']['oldest_id'] = id_url.search(first).group(1)

    with open('settings.ini', 'w') as settings:
        config.write(settings)
