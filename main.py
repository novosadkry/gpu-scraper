from CZC import CZC
from Alza import Alza
from scraper import Scraper
from product import Product
from product import onProductFetch

import threading

def scraperThread(scraper: Scraper):
    while True:
        scraper.scrape(onProductFetch)


alzaThread = threading.Thread(target = scraperThread, args = (Alza(), ))
czcThread = threading.Thread(target = scraperThread, args = (CZC(), ))

alzaThread.start()
czcThread.start()

alzaThread.join()
czcThread.join()