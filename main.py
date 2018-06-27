import re
from spider import *

running = True

# Loop To Receive URL
while running:

    url = input('Please enter URL you would like to crawl:\n\n')
    pattern = re.compile('^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$')

    if pattern.match(url):
        spider = Spider(url)
        running = False
    else:
        print('INVALID URL!')