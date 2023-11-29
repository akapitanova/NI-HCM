#!/usr/bin/env python3

import requests

from bs4 import BeautifulSoup

with open('./pp-links', 'r') as links_file:
    lines = links_file.readlines()

    for link in lines:
        link = link.lstrip().rstrip()

        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            t = soup.find('h1').get_text()
        except:
            t = f'FIXME: {link}'

        try:
            lp = soup.find('p', class_='clkPerex').get_text()
        except:
            lp = f'FIXME: {link}'

        print(f'{t};{lp}')
