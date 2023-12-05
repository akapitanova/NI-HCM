import requests
import datetime
from bs4 import BeautifulSoup as bs
from collections import defaultdict
import datetime

class Article:
    def __init__(self, url='', datetime=datetime.date.today(), title='', abstract=''):
        self.url = url
        self.datetime = datetime
        self.title = title
        self.abstract = abstract

    def __str__(self):
        return f'Article title: [{self.title}]\n\turl [{self.url}]\n\tpublished on [{self.datetime}]\n\tabstract: [{self.abstract}]\n'
    
    def __repr__(self):
        return f'Article title: [{self.title}]\n\turl [{self.url}]\n\tpublished on [{self.datetime}]\n\tabstract: [{self.abstract}]\n'


class Scraper:
    def __init__(self, first_date, one_week_later):
        self.first_date = first_date
        self.one_week_later = one_week_later
        self.articles = defaultdict(list)

# ---------------------------------------------------------- IDNES ----------------------------------------------------------
    def getOpenerIdnes(self, url):
            page = requests.get(url)
            soup = bs(page.content, 'html.parser')
            a = soup.find(class_='opener').text.strip()
            return a
    
    def scrapeIdnes(self, from_web, main_url, page_counter):
            print('==========================')
            print('Scraping: ' + from_web)
            print('==========================')
            scrape = True
            while(scrape):
                page = requests.get(main_url.format(page_counter))
                page_counter -= 1
                soup = bs(page.content, 'html.parser')
                articles = soup.find_all(class_='art')
                articles = reversed(articles)

                for a in articles:
                    date = a.find(class_='time').get('datetime')
                    date = datetime.datetime.strptime(date[0:10], '%Y-%M-%d').date()
                    if date < self.first_date:
                        continue
                    if date > self.one_week_later:
                        scrape = False
                        break
                    url = a.find(class_='art-link').get('href')
                    title = a.find(class_='art-link').text.strip()
                    if not 'OBRAZEM:' in title:
                        art = self.getOpenerIdnes(url)
                        self.articles[from_web].append(Article(url=url, datetime=date, title=title, abstract=art))

# ---------------------------------------------------------- LIDOVKY  ----------------------------------------------------------
    def getOpenerLidovky(self, url):
            page = requests.get(url)
            soup = bs(page.content, 'html.parser')
            a = soup.find(class_='opener').text.strip()
            return a

    def scrapeLidovky(self, from_web, main_url, page_counter):
            print('==========================')
            print('Scraping: ' + from_web)
            print('==========================')
            scrape = True
            while(scrape):
                page = requests.get(main_url.format(page_counter))
                page_counter -= 1
                soup = bs(page.content, 'html.parser')
                articles = soup.find_all(class_='art')
                articles = reversed(articles)

                for a in articles:
                    date = a.find(class_='time').get('datetime')
                    date = datetime.datetime.strptime(date[0:10], '%Y-%M-%d').date()
                    if date < self.first_date:
                        continue
                    if date > self.one_week_later:
                        scrape = False
                        break
                    url = a.find(class_='art-link').get('href')
                    title = a.find('h3').text.strip()
                    if not 'OBRAZEM:' in title:
                        art = self.getOpenerLidovky(url)
                        self.articles[from_web].append(Article(url=url, datetime=date, title=title, abstract=art))

# ---------------------------------------------------------- AKTUALNE  ----------------------------------------------------------
    def getOpenerAktualne(self, url):
            page = requests.get(url)
            soup = bs(page.content, 'html.parser')
            a = soup.find(class_='article__perex').text.strip()
            if a == '' :
                 a = soup.find('p').text.strip()
            return a

    def scrapeAktualne(self, from_web, main_url, page_counter):
            print('==========================')
            print('Scraping: ' + from_web)
            print('==========================')
            scrape = True
            while(scrape):
                page = requests.get(main_url.format(page_counter))
                page_counter -= 20
                soup = bs(page.content, 'html.parser')

                articles = soup.find_all(class_='small-box filter-b-site-aktualne clearfix')
                articles = reversed(articles)

                for a in articles:
                    tmp = a.find(class_='timeline__label').text.strip().split()
                    if tmp [0] == 'Aktualizováno':
                         date = ''.join(tmp[1:4])
                    else:
                        date = ''.join(tmp[:3])
                    date = datetime.datetime.strptime(date, '%d.%M.%Y').date()
                    if date < self.first_date:
                        continue
                    if date > self.one_week_later:
                        scrape = False
                        break
                    url = 'https://zpravy.aktualne.cz/' + a.find('a').get('href')
                    title = a.find('h3').text.strip()
                    art = self.getOpenerAktualne(url)
                    self.articles[from_web].append(Article(url=url, datetime=date, title=title, abstract=art))

                articles = soup.find_all(class_='swift-box__wrapper filter-b-site-aktualne')
                articles = reversed(articles)
                for a in articles:
                    tmp = a.find(class_='timeline__label').text.strip().split()
                    if tmp [0] == 'Aktualizováno':
                         date = ''.join(tmp[1:4])
                    else:
                        date = ''.join(tmp[:3])
                    date = datetime.datetime.strptime(date, '%d.%M.%Y').date()
                
                    if date < self.first_date:
                        continue
                    if date > self.one_week_later:
                        scrape = False
                        break
                    url = 'https://zpravy.aktualne.cz/' + a.find('a').get('href')
                    title = a.find('h3').text.strip()
                    art = self.getOpenerAktualne(url)
                    self.articles[from_web].append(Article(url=url, datetime=date, title=title, abstract=art))

# ---------------------------------------------------------- ac24  ----------------------------------------------------------
    def getOpenerAC24(self, url):
            page = requests.get(url)
            soup = bs(page.content, 'html.parser')
            a = soup.find('p').text.strip()
            return a

    def scrapeAC24(self, from_web, main_url, page_counter):
            print('==========================')
            print('Scraping: ' + from_web)
            print('==========================')
            scrape = True
            while(scrape):
                page = requests.get(main_url.format(page_counter))
                page_counter -= 1
                soup = bs(page.content, 'html.parser')
                articles = soup.find_all(class_='column post-column small-mb-2 large-mb-4 hor-sep-b')
                articles = reversed(articles)

                for a in articles:
                    date = a.find(class_='entry-date published').get('datetime')
                    date = datetime.datetime.strptime(date[0:10], '%Y-%M-%d').date()
                    if date < self.first_date:
                        continue
                    if date > self.one_week_later:
                        scrape = False
                        break
                    title = a.find('h2').text.strip()
                    url = a.find(class_='hover-line').get('href')
                    art = self.getOpenerAC24(url)
                    self.articles[from_web].append(Article(url=url, datetime=date, title=title, abstract=art))

# ---------------------------------------------------------- czechfreepress  ----------------------------------------------------------
   
    def getOpenerCzechFreePress(self, url):
        page = requests.get(url)
        soup = bs(page.content, 'html.parser')
        a = soup.find(class_='f2c-introtext').find('p').text
        a = a.rstrip()
        a = a.replace('\n', '')
        a = a.replace('\r', '')
        a = a.replace('<br/>', '')
        return a
    
    def scrapeCzechFreePress(self, from_web, main_url, page_counter):
            print('==========================')
            print('Scraping: ' + from_web)
            print('==========================')
            scrape = True
            rep = {'leden': 'January', 'únor': 'February','prosinec': 'December'}
            while(scrape):
                page = requests.get(main_url.format(page_counter))
                page_counter -= 1
                soup = bs(page.content, 'html.parser')
                articles = soup.find_all(class_='item-inner clearfix')
                articles = reversed(articles)
                for a in articles:
                    if a.find(class_='counter') != None:
                         continue
                    date = a.find(class_='published').text.strip()
                    date = date[:-1]
                    for i, j in rep.items():
                        date = date.replace(i, j)
                    date = datetime.datetime.strptime(date, '%d. %B %Y').date()
                    if date < self.first_date:
                        continue
                    if date > self.one_week_later:
                        scrape = False
                        break
                    title = a.find('h2').text.strip()
                    url = 'https://www.czechfreepress.cz/' + a.find('h2').find('a').get('href')
                    art = self.getOpenerCzechFreePress(url)
                    self.articles[from_web].append(Article(url=url, datetime=date, title=title, abstract=art))


if __name__ == '__main__':
    scraper = Scraper(datetime.date(2023, 1, 1), datetime.date(2023, 1, 1) + datetime.timedelta(days=7))
    
    scraper.scrapeIdnes(from_web='idnes.cz', main_url='https://www.idnes.cz/zpravy/domaci/{}', page_counter=175)
    scraper.scrapeLidovky(from_web='lidovky.cz', main_url='https://www.lidovky.cz/archiv/{}', page_counter=448)
    scraper.scrapeAktualne(from_web='aktualne.cz', main_url='https://zpravy.aktualne.cz/domaci/?offset={}', page_counter=3860)
    scraper.scrapeAC24(from_web='ac24.cz', main_url='https://www.ac24.cz/page/{}', page_counter=324)
    scraper.scrapeCzechFreePress(from_web='czechfreepress.cz', main_url='https://www.czechfreepress.cz/z-domova/z-domova/blog.html?page={}', page_counter=11)
    print(scraper.articles)

    f = open('Articles.csv', 'w')
    f.writelines('Web;Title;Url;Datetime;Abstract\n')
    for articles, web in zip(scraper.articles.values(), scraper.articles.keys()):
        for article in articles:
            f.write(web + ';' + article.title + ';' + article.url + ';' + str(article.datetime) + ';' + article.abstract + '\n' )
    f.close()

    # špatně  Seznam zpravy, BBC, - jednotlive clanky nacitanmy scriptem, nelze iterovat pres nejake cislo stranky CZ24News, - cela stranka nacitana scriptem, nelze z toho nic ziskat
    # Aeronet - velmi pomaly web, je potřeba nějaký sleep, bez sleepu ten web spadne, vrací <td>Block reason:</td><td><span>Bad bot access attempt.</span></td></tr>