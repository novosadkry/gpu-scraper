from CZC import CZC
from Alza import Alza
from scraper import Scraper
from product import Product
from product import onProductFetch

import threading
import time

def scraperThread(scraper: Scraper):
    while True:
        scraper.scrape(onProductFetch)


if __name__ == '__main__':
    alzaThread = threading.Thread(target = scraperThread, args = (Alza(), ))
    czcThread = threading.Thread(target = scraperThread, args = (CZC(), ))

    alzaThread.daemon = True
    czcThread.daemon = True

    alzaThread.start()
    czcThread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
