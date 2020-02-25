import requests
from bs4 import BeautifulSoup

URL = "https://www.fanfiction.net/misc/Misc-Comics/"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')

print(soup.prettify())


# https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/
