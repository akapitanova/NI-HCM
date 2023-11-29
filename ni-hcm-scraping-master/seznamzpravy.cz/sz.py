#!/usr/bin/env python3

import csv
import requests

from bs4 import BeautifulSoup

with open('./seznamzpravy.cz-links-3.csv', 'r') as csv_file:
    reader = csv.reader(csv_file, delimiter='~')

    for link, title in reader:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            t = soup.find('h1', class_='e_V e_N d_gZ').get_text()
        except:
            t = f'FIXME: {link}'

        lp_elem = soup.find('p', class_='e_ac d_fs')

        if not lp_elem:
            lp_elem = soup.find('span', class_='e_B')

        try:
            lp = lp_elem.get_text()
        except:
            lp = f'FIXME: {link}'

        print(f'{t};{lp}')
