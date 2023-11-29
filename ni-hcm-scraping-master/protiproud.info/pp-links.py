#!/usr/bin/env python3

import csv
import requests

from bs4 import BeautifulSoup

# from 1 to 10
for i in range(1, 11):
    page = requests.get(f'https://protiproud.info/?pg={i}')
    soup = BeautifulSoup(page.content, 'html.parser')

    hs = soup.find_all('h2')[:10]

    for h in hs:
        a = h.find('a')
        print(a['href'])
