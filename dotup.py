import re
import requests
from bs4 import BeautifulSoup
import configparser
import sys


config = configparser.ConfigParser()
config.read('settings.ini')

oldest_id = config['Files']['oldest_id']

# This regular expression returns the file IDs
id_url = re.compile(r'org([0-9]+.[a-z0-9]{1,4})')
id_num = re.compile(r'([0-9]+).[a-z0-9]{1,4}')


def get_page(page_number='', mode='default'):

    if mode == 'light':
        req = requests.get('http://light.dotup.org/' + page_number)

    else:
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


def output_url(output_file, input_list, mode='default'):
    with open(output_file, 'a') as url_list:
        for i in input_list:

            if mode == 'light':
                url_list.write('http://www.light.dotup.org/uploda/www.dotup.org' + i + '\n')

            else:
                url_list.write('http://www.dotup.org/uploda/www.dotup.org' + i + '\n')


def crawler(count='', links=[], files=[], mode='default'):
    h = get_page(count, mode=mode)
    get_links(h, links)
    filter_links(links, files)


def main(mode="default"):

    links = []
    files = []
    counter = 2
    page = str(counter) + '.html'

    if mode == 'light':
        maximum = 250

    else:
        maximum = 309

    open('url_list.txt', 'w').close()

    crawler(links=links, files=files, mode=mode)

    if oldest_id in files:
        id_index = files.index(oldest_id)
        final = files[:id_index]
        output_url('url_list.txt', final, mode=mode)
    else:
        output_url('url_list.txt', files, mode=mode)

    while oldest_id not in files:
        files = []
        crawler(page, links=links, files=files, mode=mode)

        if oldest_id in files:
            id_index = files.index(oldest_id)
            final = files[:id_index]
            output_url('url_list.txt', final, mode=mode)
            break

        else:

            if int(id_num.search(files[-1]).group(1)) < int(id_num.search(oldest_id).group(1)):
                files = [x.group(0) for f in files for x in [id_num.search(f)]
                         if int(x.group(1)) > int(id_num.search(oldest_id).group(1))]
                output_url('url_list.txt', files, mode=mode)
                break

            elif counter != maximum:
                output_url('url_list.txt', files, mode=mode)
                counter += 1
                page = str(counter) + '.html'

            else:
                break

    with open('url_list.txt', 'r') as url_list:
        first = url_list.readline()
        config['Files']['oldest_id'] = id_url.search(first).group(1)

    with open('settings.ini', 'w') as settings:
        config.write(settings)

if __name__ == '__main__':

    if len(sys.argv) == 2:
        main(sys.argv[1])

    else:
        main()
