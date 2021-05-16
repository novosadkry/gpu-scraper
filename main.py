from CZC import CZC
from Alza import Alza
from TSBohemia import TSBohemia

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
    tsThread = threading.Thread(target = scraperThread, args = (TSBohemia(), ))

    alzaThread.daemon = True
    czcThread.daemon = True
    tsThread.daemon = True

    alzaThread.start()
    czcThread.start()
    tsThread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
