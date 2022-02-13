import cloudscraper
import requests
import os
import csv
import sys
from bs4 import BeautifulSoup

# https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/

# create a cloudscraper instance
scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})

base_url = 'https://www.fanfiction.net/'

if len(sys.argv) > 1:
        if sys.argv[1] == "ccs":
            output_filename = 'output_ccs'
            urls = ['https://www.fanfiction.net/anime/Card-Captor-Sakura/?&srt=1&lan=1&r=4', 'https://www.fanfiction.net/anime/Card-Captor-Sakura/?&srt=1&lan=1&r=4&p=2', 'https://www.fanfiction.net/anime/Card-Captor-Sakura/?&srt=1&lan=1&r=4&p=6', 'https://www.fanfiction.net/anime/Card-Captor-Sakura/?&srt=1&lan=1&r=103&p=2', 'https://www.fanfiction.net/anime/Card-Captor-Sakura/?&srt=1&lan=1&r=103', 'https://www.fanfiction.net/anime/Card-Captor-Sakura/?&srt=1&lan=1&r=103&p=3', 'https://www.fanfiction.net/anime/Card-Captor-Sakura/?&srt=1&lan=1&r=103&p=4']
        
        elif sys.argv[1] == "op":
            output_filename = 'output_op'
            urls = ['https://www.fanfiction.net/anime/One-Piece/?&srt=1&r=103', 'https://www.fanfiction.net/anime/One-Piece/?&srt=1&r=103&p=2', 'https://www.fanfiction.net/anime/One-Piece/?&srt=1&r=103&p=3', 'https://www.fanfiction.net/anime/One-Piece/?&srt=1&r=103&p=4']
            
        elif sys.argv[1] == "marvel":
            output_filename = 'output_marvel'
            urls = ['https://www.fanfiction.net/comic/Marvel/?&srt=1&lan=1&r=103&p=2', 'https://www.fanfiction.net/comic/Marvel/?&srt=1&lan=1&r=103', 'https://www.fanfiction.net/comic/Marvel/?&srt=1&lan=1&r=103&p=3', 'https://www.fanfiction.net/comic/Marvel/?&srt=1&lan=1&r=103&p=4']

fanfics = []

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for url in urls:
    response = scraper.get(url).text
    response_html = BeautifulSoup(response, 'html5lib')

    table = response_html.find('div', attrs={'id': 'content_wrapper_inner'})

    for row in table.findAll('div', attrs={'class': 'z-list zhover zpointer'}):
        fanfic = {}
        fanfic['title'] = row.find('a', attrs={'class': 'stitle'}).text
        fanfic['picture'] = row.img['src']
        fanfic['author'] = row.select_one("a[href*='u']").text
        fanfic['synopsis'] = row.select_one(
            "div[class='z-indent z-padtop']").text.split('Rated')[0]
        # fanfic['options'] = row.find('div', attrs={'class': 'z-padtop2 xgray'}).text
        fanfic['classement'] = row.find(
            'div', attrs={'class': 'z-padtop2 xgray'}).text.split('-')[0]
        fanfic['language'] = row.find(
            'div', attrs={'class': 'z-padtop2 xgray'}).text.split('-')[1]
        fanfic['genre'] = row.find(
            'div', attrs={'class': 'z-padtop2 xgray'}).text.split('-')[2]
        fanfic['link_fanfic'] = row.a['href']
        fanfics.append(fanfic)
        # print(row.prettify())
        # print(fanfics)
        print(fanfic)

        for fanfic in fanfics:
            filename = os.path.join(
                BASE_DIR, f'fanfics/management/commands/{output_filename}.csv')
            with open(filename, 'w', newline='') as f:
                w = csv.DictWriter(f, ['title', 'picture', 'author', 'synopsis',
                                       'classement', 'language', 'genre', 'link_fanfic'])
                w.writeheader()
                for fc in fanfics:
                    w.writerow(fc)

    # filename = 'fanfictions_scraping.csv'
    # with open(filename, 'w', newline='') as f:
    #     w = csv.DictWriter(f, ['title', 'picture', 'author', 'synopsis',
    #                            'classement', 'language', 'genre', 'link_fanfic'])
    #     w.writeheader()
    #     for fanfic in fanfics:
    #         w.writerow(fanfic)
