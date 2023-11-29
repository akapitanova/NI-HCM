#!/usr/bin/env python3

import feedparser
import os

for f in os.listdir('./rss'):
    filename = f'./rss/{f}'

    feed = feedparser.parse(filename)

    entries = feed.entries

    for e in entries:
        print(f'{e.title};{e.summary}')
