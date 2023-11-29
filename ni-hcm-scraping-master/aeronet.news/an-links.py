#!/usr/bin/env python3

import csv
import requests
import time
import random

from bs4 import BeautifulSoup

# from 1 to 10
for i in range(1, 11):
    with open(f'./an{i}.html', 'r') as f:
      page = f.read()
      soup = BeautifulSoup(page, 'html.parser')

      hs = soup.find_all('h3', class_='entry-title')[:10]

      for h in hs:
          a = h.find('a')
          print(a['href'])
