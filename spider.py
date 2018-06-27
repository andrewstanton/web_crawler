import sys
import urllib.request
from urllib.parse import *
import bs4 as bs

class Spider():
    def __init__(self, url):
        self.parsedURL = urllib.parse.urlparse(url)
        
        # Variables For Crawl
        self.pages = set()
        self.valid_pages = set()
        self.query_pages = 0

        self.crawl_init(self.parsedURL.path.strip('/'))
        pass

    def crawl_init(self, initPage):
        self.crawl_page(initPage)
        self.write_to_text_file()
        print('Crawl Finished!')

    # Crawling Given Page
    def crawl_page(self, path):

        sys.stdout.write('Crawled: {0}\r'.format(len(self.pages)))
        sys.stdout.flush()

        # add to set to mark crawled
        self.pages.add(path)

        url = self.parsedURL.scheme + '://' + self.parsedURL.netloc + '/' + path

        try:
            response = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            print('Error Code: ', e.code)
            return
        except urllib.error.URLError as e:
            print('Error: ', e.reason)
            return
        else:
            self.valid_pages.add(path)

        sauce = response.read()
        soup = bs.BeautifulSoup(sauce, 'lxml')

        # loop thru all links on the page
        for link in soup.find_all('a'):
            href = link.get('href')
            parsedHref = urllib.parse.urlparse(href)

            # if url is not an external url
            if (parsedHref.netloc == self.parsedURL.netloc or parsedHref.netloc == '') and not isinstance(parsedHref.path, bytes) and parsedHref.scheme == '':
                stripHref = parsedHref.path.strip('/')
                
                # add query params if any
                if parsedHref.query:
                    scanned = stripHref + '/?' + parsedHref.query
                else:
                    scanned = stripHref

                # scan if not in pages set
                if scanned not in self.pages:
                    if parsedHref.query:
                        self.query_pages = int(self.query_pages) + 1
                    
                    self.crawl_page(scanned)

    def write_to_text_file(self):
        with open('site.txt', 'w') as out_file:
            out_file.write(str(self.parsedURL.netloc) + ' Crawl Export\n')
            out_file.write('Total Pages: ' + str(len(self.valid_pages)) + '\n')
            out_file.write('Query Pages: ' + str(self.query_pages) + '\n\n')

            sorted_pages = sorted(self.pages)

            for page in sorted_pages:
                out_file.write(str(self.parsedURL.netloc + '/' + page) + '\n')