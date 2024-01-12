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
            a = a.replace('\n', '')
            a = a.replace('\r', '')
            a = a.replace('\t', ',')
            a = a.replace(';', ',')
            a = a.replace('<br/>', '')
            return a
    
    def scrapeIdnes(self, from_web, main_url, page_counter):
            print('==========================')
            print('Scraping: ' + from_web)
            print('==========================')
            scrape = True
            while(scrape):
                page = requests.get(main_url.format(page_counter))
                print(f'scraping page {page_counter}')
                page_counter -= 1
                soup = bs(page.content, 'html.parser')
                articles = soup.find_all(class_='art')
                articles = reversed(articles)
                for a in articles:
                    date = a.find(class_='time').get('datetime')
                    date = datetime.datetime.strptime(date[0:10], '%Y-%m-%d').date()
                    if date < self.first_date:
                        continue
                    if date > self.one_week_later:
                        scrape = False
                        break
                    url = a.find(class_='art-link').get('href')
                    title = a.find(class_='art-link').text.strip()
                    title = title.replace('\n', '')
                    title = title.replace('\r', '')
                    title = title.replace('\t', ',')
                    title = title.replace(';', ',')
                    title = title.replace('<br/>', '')
                    print(title)
                    if not 'OBRAZEM:' in title:
                        art = self.getOpenerIdnes(url)                        
                        self.articles[from_web].append(Article(url=url, datetime=date, title=title, abstract=art))

# ---------------------------------------------------------- LIDOVKY  ----------------------------------------------------------
    def getOpenerLidovky(self, url):
            page = requests.get(url)
            soup = bs(page.content, 'html.parser')
            a = soup.find(class_='opener').text.strip()
            a = a.replace('\n', '')
            a = a.replace('\r', '')
            a = a.replace('\t', ',')
            a = a.replace(';', ',')
            a = a.replace('<br/>', '')
            return a

    def scrapeLidovky(self, from_web, main_url, page_counter):
            print('==========================')
            print('Scraping: ' + from_web)
            print('==========================')
            scrape = True
            while(scrape):
                page = requests.get(main_url.format(page_counter))
                print(f'scraping page {page_counter}')
                page_counter -= 1
                soup = bs(page.content, 'html.parser')
                articles = soup.find_all(class_='art')
                articles = reversed(articles)

                for a in articles:
                    date = a.find(class_='time').get('datetime')
                    date = datetime.datetime.strptime(date[0:10], '%Y-%m-%d').date()
                    if date < self.first_date:
                        continue
                    if date > self.one_week_later:
                        scrape = False
                        break
                    url = a.find(class_='art-link').get('href')
                    title = a.find('h3').text.strip()
                    title = title.replace('\n', '')
                    title = title.replace('\r', '')
                    title = title.replace('\t', ',')
                    title = title.replace(';', ',')
                    title = title.replace('<br/>', '')
                    print(title)
                    obrazem = a.find(class_='brisk')
                    if obrazem != None:
                        obrazem = obrazem.text
                    else: obrazem = 'NOT_OBRAZEM_VALUE'
                    if (not 'OBRAZEM:' in title) and ('Obrazem' not in obrazem):
                        art = self.getOpenerLidovky(url)
                        self.articles[from_web].append(Article(url=url, datetime=date, title=title, abstract=art))

# ---------------------------------------------------------- AKTUALNE  ----------------------------------------------------------
    def getOpenerAktualne(self, url):
            page = requests.get(url)
            soup = bs(page.content, 'html.parser')
            a = soup.find(class_='article__perex')
            if a == None :
                 a = soup.find('p').text.strip()
            else: a = a.text.strip()
            a = a.replace('\n', '')
            a = a.replace('\r', '')
            a = a.replace('\t', ',')
            a = a.replace(';', ',')
            a = a.replace('<br/>', '')
            return a

    def scrapeAktualne(self, from_web, main_url, page_counter):
            print('==========================')
            print('Scraping: ' + from_web)
            print('==========================')
            scrape = True
            while(scrape):
                page = requests.get(main_url.format(page_counter))
                print(f'scraping page {page_counter}')
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
                    date = datetime.datetime.strptime(date, '%d.%m.%Y').date()
                    if date < self.first_date:
                        continue
                    if date > self.one_week_later:
                        scrape = False
                        break
                    url = 'https://zpravy.aktualne.cz/' + a.find('a').get('href')
                    title = a.find('h3').text.strip()
                    title = title.replace('\n', '')
                    title = title.replace('\r', '')
                    title = title.replace('\t', ',')
                    title = title.replace(';', ',')
                    title = title.replace('<br/>', '')
                    print(title)
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
                    date = datetime.datetime.strptime(date, '%d.%m.%Y').date()
                
                    if date < self.first_date:
                        continue
                    if date > self.one_week_later:
                        scrape = False
                        break
                    url = 'https://zpravy.aktualne.cz/' + a.find('a').get('href')
                    title = a.find('h3').text.strip()
                    title = title.replace('\n', '')
                    title = title.replace('\r', '')
                    title = title.replace('\t', ',')
                    title = title.replace(';', ',')
                    title = title.replace('<br/>', '')
                    print(title)
                    art = self.getOpenerAktualne(url)
                    self.articles[from_web].append(Article(url=url, datetime=date, title=title, abstract=art))

# ---------------------------------------------------------- ac24  ----------------------------------------------------------
    def getOpenerAC24(self, url):
            page = requests.get(url)
            soup = bs(page.content, 'html.parser')
            a = soup.find('p').text.strip()
            a = a.replace('\n', '')
            a = a.replace('\r', '')
            a = a.replace('\t', ',')
            a = a.replace(';', ',')
            a = a.replace('<br/>', '')
            return a

    def scrapeAC24(self, from_web, main_url, page_counter):
            print('==========================')
            print('Scraping: ' + from_web)
            print('==========================')
            scrape = True
            while(scrape):
                page = requests.get(main_url.format(page_counter))
                print(f'scraping page {page_counter}')
                page_counter -= 1
                soup = bs(page.content, 'html.parser')
                articles = soup.find_all(class_='column post-column small-mb-2 large-mb-4 hor-sep-b')
                articles = reversed(articles)

                for a in articles:
                    date = a.find(class_='entry-date published').get('datetime')
                    date = datetime.datetime.strptime(date[0:10], '%Y-%m-%d').date()
                    if date < self.first_date:
                        continue
                    if date > self.one_week_later:
                        scrape = False
                        break
                    title = a.find('h2').text.strip()
                    title = title.replace('\n', '')
                    title = title.replace('\r', '')
                    title = title.replace('\t', ',')
                    title = title.replace(';', ',')
                    title = title.replace('<br/>', '')
                    print(title)
                    url = a.find(class_='hover-line').get('href')
                    art = self.getOpenerAC24(url)
                    self.articles[from_web].append(Article(url=url, datetime=date, title=title, abstract=art))

# ---------------------------------------------------------- czechfreepress  ----------------------------------------------------------
   
    def getOpenerCzechFreePress(self, url):
        page = requests.get(url)
        soup = bs(page.content, 'html.parser',from_encoding="UTF-8")
        a = soup.find(class_='f2c-introtext').find('p').text
        a = a.rstrip()
        a = a.replace('\n', '')
        a = a.replace('\r', '')
        a = a.replace('\t', ',')
        a = a.replace(';', ',')
        a = a.replace('<br/>', '')
        return a
    
    def scrapeCzechFreePress(self, from_web, main_url, page_counter):
            print('==========================')
            print('Scraping: ' + from_web)
            print('==========================')
            scrape = True
            rep = {'leden': 'January', 'únor': 'February','prosinec': 'December','listopad': 'November'}
            while(scrape):
                page = requests.get(main_url.format(page_counter))
                print(f'scraping page {page_counter}')
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
                    title = title.replace('\n', '')
                    title = title.replace('\r', '')
                    title = title.replace('\t', ',')
                    title = title.replace(';', ',')
                    title = title.replace('<br/>', '')
                    print(title)
                    url = 'https://www.czechfreepress.cz/' + a.find('h2').find('a').get('href')
                    art = self.getOpenerCzechFreePress(url)
                    self.articles[from_web].append(Article(url=url, datetime=date, title=title, abstract=art))

# ---------------------------------------------------------- pravdive.eu  ----------------------------------------------------------
   
    def getOpenerPravdiveEU(self, url):
        page = requests.get(url)
        soup = bs(page.content, 'html.parser',from_encoding="UTF-8")
        a = soup.find(class_='article-content').text.strip()
        a = a.replace('\n', '')
        a = a.replace('\r', '')
        a = a.replace('\t', ',')
        a = a.replace(';', ',')
        a = a.replace('<br/>', '')
        return a
    
    def scrapePravdiveEU(self, from_web, main_url, page_counter):
            print('==========================')
            print('Scraping: ' + from_web)
            print('==========================')
            scrape = True
            while(scrape):
                page = requests.get(main_url.format(page_counter))
                print(f'scraping page {page_counter}')
                page_counter -= 1
                soup = bs(page.content, 'html.parser',from_encoding="UTF-8")
                articles = soup.find_all(class_='first-section-news')
                articles = reversed(articles)
                for a in articles:
                    date = a.find(class_='article-meta hidden-xs').text.strip().split('\n')
                    date = date[0]
                    date = datetime.datetime.strptime(date, '%d-%m-%Y').date()
                    if date < self.first_date:
                        continue
                    if date > self.one_week_later:
                        scrape = False
                        break
                    title = a.find(class_='col-md-8 col-xs-9').text.strip().split('\n')
                    title = title[0]
                    title = title.replace('\n', '')
                    title = title.replace('\r', '')
                    title = title.replace('\t', ',')
                    title = title.replace(';', ',')
                    title = title.replace('<br/>', '')
                    print(title)
                    url = 'https://pravdive.eu/' + a.find(class_='col-md-8 col-xs-9').find('a').get('href')
                    art = self.getOpenerPravdiveEU(url)
                    self.articles[from_web].append(Article(url=url, datetime=date, title=title, abstract=art))


# ---------------------------------------------------------- zvedavec.news  ----------------------------------------------------------
   
    def getOpenerZvedavec(self, url):
        page = requests.get(url)
        soup = bs(page.content, 'html.parser',from_encoding="UTF-8")
        a = soup.find('p').text.strip()
        a = a.replace('\n', '')
        a = a.replace('\r', '')
        a = a.replace('\t', ',')
        a = a.replace(';', ',')
        a = a.replace('<br/>', '')
        return a
    
    def scrapeZvedavec(self, from_web, main_url):
            print('==========================')
            print('Scraping: ' + from_web)
            print('==========================')
            page = requests.get(main_url)
            soup = bs(page.content, 'html.parser',from_encoding="UTF-8")
            articles = soup.find(class_='seznam-clanku').find_all('tr')
            for a in articles:
                data = a.text.strip().split('\n')
                if data[0] == 'Titulek': continue
                # print(data)
                date = data[3]
                date = datetime.datetime.strptime(date, '%d.%m.%Y').date()
                if date > self.one_week_later: continue                 
                title = data[0]
                title = title.replace('\n', '')
                title = title.replace('\r', '')
                title = title.replace('\t', ',')
                title = title.replace(';', ',')
                title = title.replace('<br/>', '')
                print(title)
                url = 'https://zvedavec.news/' + a.find('a').get('href')
                art = self.getOpenerZvedavec(url)
                self.articles[from_web].append(Article(url=url, datetime=date, title=title, abstract=art))

# ---------------------------------------------------------- novarepublika.eu  ----------------------------------------------------------
   
    def getOpenerNovaRepublika(self, url):
        page = requests.get(url)
        soup = bs(page.content, 'html.parser',from_encoding="UTF-8")
        a = soup.find_all('p')
        retval = ''
        for p in a:
            p = p.text
            if len(p) < 50: continue
            else:
                retval = p.replace('\n', '')
                retval = retval.replace('\r', '')
                retval = retval.replace('\t', ',')
                retval = retval.replace(';', ',')
                retval = retval.replace('<br/>', '')
                break
        return retval
    
    def scrapeNovaRepublika(self, from_web, main_url, page_counter):
            print('==========================')
            print('Scraping: ' + from_web)
            print('==========================')
            scrape = True
            rep = {'ledna': 'January', 'února': 'February','prosince': 'December'}
            while(scrape):
                page = requests.get(main_url.format(page_counter))
                print(f'scraping page {page_counter}')
                page_counter -= 1
                soup = bs(page.content, 'html.parser',from_encoding="UTF-8")
                articles = soup.find_all(class_='article-info-wrapper')
                articles = reversed(articles)
                for a in articles:
                    date = a.find(class_='article-date').text.strip()
                    for i, j in rep.items():
                        date = date.replace(i, j)
                    date = datetime.datetime.strptime(date, '%d. %B %Y').date()
                    if date < self.first_date:
                        continue
                    if date > self.one_week_later:
                        scrape = False
                        break
                    title = a.find('h3').text.strip()
                    title = title.replace('\n', '')
                    title = title.replace('\r', '')
                    title = title.replace('\t', ',')
                    title = title.replace(';', ',')
                    title = title.replace('<br/>', '')
                    url =  a.find('h3').find('a').get('href')
                    art = self.getOpenerNovaRepublika(url)
                    self.articles[from_web].append(Article(url=url, datetime=date, title=title, abstract=art))

# ---------------------------------------------------------- novarepublika.eu  ----------------------------------------------------------
   
    def getOpenerParlamentniListy(self, url):
        page = requests.get(url)
        soup = bs(page.content, 'html.parser',from_encoding="UTF-8")
        a = soup.find('p').text
        a = a.replace('\n', '')
        a = a.replace('\r', '')
        a = a.replace('\t', ',')
        a = a.replace(';', ',')
        a = a.replace('<br/>', '')  
        return a
    
    def scrapeParlamentniListy(self, from_web, main_url, page_counter):
            print('==========================')
            print('Scraping: ' + from_web)
            print('==========================')
            scrape = True
            while(scrape):
                page = requests.get(main_url.format(page_counter))
                print(f'scraping page {page_counter}')
                page_counter -= 1
                soup = bs(page.content, 'html.parser',from_encoding="UTF-8")
                articles = soup.find(class_='section-brown articles-list').find_all('li')
                for a in articles:
                    if a.find(class_='time') == None: continue
                    date = a.find(class_='time').text.strip()
                    date = date[0:10]
                    date = datetime.datetime.strptime(date, '%d.%m.%Y').date()
                    if date < self.first_date:
                        continue
                    if date > self.one_week_later:
                        scrape = False
                        break
                    title = a.find('h2').text.strip()
                    title = title.replace('\n', '')
                    title = title.replace('\r', '')
                    title = title.replace('\t', ',')
                    title = title.replace(';', ',')
                    title = title.replace('<br/>', '')
                    print(title)
                    url =  'https://www.parlamentnilisty.cz' + a.find('a').get('href')
                    art = self.getOpenerParlamentniListy(url)
                    self.articles[from_web].append(Article(url=url, datetime=date, title=title, abstract=art))


if __name__ == '__main__':
    scraper = Scraper(datetime.date(2023, 1, 1), datetime.date(2023, 1, 1) + datetime.timedelta(days=30))
    f = open('Arts.csv', 'w')
    f.writelines('Web;Title;Url;Datetime;Abstract\n')
    scraper.scrapeIdnes(from_web='idnes.cz', main_url='https://www.idnes.cz/zpravy/domaci/{}', page_counter=194)
    scraper.scrapeLidovky(from_web='lidovky.cz', main_url='https://www.lidovky.cz/archiv/{}', page_counter=497)
    scraper.scrapeAktualne(from_web='aktualne.cz', main_url='https://zpravy.aktualne.cz/domaci/?offset={}', page_counter=4280)
    scraper.scrapeAC24(from_web='ac24.cz', main_url='https://www.ac24.cz/page/{}', page_counter=352)
    scraper.scrapeCzechFreePress(from_web='czechfreepress.cz', main_url='https://www.czechfreepress.cz/z-domova/z-domova/blog.html?page={}', page_counter=13)
    scraper.scrapePravdiveEU(from_web='pravdive.cz', main_url='https://pravdive.eu/category/1/zpravodajstvi?page={}', page_counter=911)
    scraper.scrapeZvedavec(from_web='zvedavec.news', main_url='https://zvedavec.news/archiv/2023/')
    scraper.scrapeNovaRepublika(from_web='novarepublika.cz', main_url='https://www.novarepublika.cz/page/{}', page_counter=233)
    scraper.scrapeParlamentniListy(from_web='parlamentnilisty.cz', main_url='https://www.parlamentnilisty.cz/archiv?p={}', page_counter=422)
    for articles, web in zip(scraper.articles.values(), scraper.articles.keys()):
            for article in articles:
                f.write(web + ';' + article.title + ';' + article.url + ';' + str(article.datetime) + ';' + article.abstract + '\n' )
    f.close()
