from CZC import CZC
from Alza import Alza
from TSBohemia import TSBohemia

from scraper import Scraper
from product import Product
from product import setupRedis
from product import loadProducts
from product import onProductFetch

from log import Severity
from log import log

import threading
import time

def scraperThread(scraper: Scraper):
    while True:
        scraper.scrape(onProductFetch)


if __name__ == '__main__':
    setupRedis(host = 'ip.zahrajto.wtf', port = 25543, password = 'tvojemama')

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
        log(Severity.FAIL, "Main", "Keyboard interrupt, exiting...")
        pass
