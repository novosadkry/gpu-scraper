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

from config import config

import threading
import time

def scraperThread(scraper: Scraper):
    while True:
        scraper.scrape(onProductFetch)

if __name__ == '__main__':
    setupRedis(
        host = config['Redis']['host'],
        port = int(config['Redis']['port']),
        password = config['Redis']['password']
    )

    alzaThread = threading.Thread(target = scraperThread, args = (Alza(int(config['Alza']['delay'])), ))
    czcThread = threading.Thread(target = scraperThread, args = (CZC(int(config['CZC']['delay'])), ))
    tsThread = threading.Thread(target = scraperThread, args = (TSBohemia(int(config['TSBohemia']['delay'])), ))

    alzaThread.daemon = True
    czcThread.daemon = True
    tsThread.daemon = True

    if config['Alza']['enabled']: alzaThread.start()
    if config['CZC']['enabled']: czcThread.start()
    if config['TSBohemia']['enabled']: tsThread.start()

    log(Severity.INFO, "Main", "Started!")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log(Severity.FAIL, "Main", "Keyboard interrupt, exiting...")
        pass
