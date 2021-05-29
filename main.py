from CZC import CZC
from Alza import Alza
from TSBohemia import TSBohemia

from scraper import Scraper

from log import Severity
from log import log
from log import logc

from config import config

import threading
import time

def scraperThread(scraper: Scraper):
    logc(Severity.DEBUG, scraper.store, "Thread started!")

    scraper.setup()
    while True:
        scraper.scrape()
        time.sleep(scraper.delay)

if __name__ == '__main__':
    try:
        log(Severity.DEBUG, "Main", "-" * 15, "LOG BEGIN", "-" * 15)
        log(Severity.INFO, "Main", "Starting up...")

        alzaThread = threading.Thread(target = scraperThread, args = (Alza(int(config['Alza']['delay'])), ))
        czcThread = threading.Thread(target = scraperThread, args = (CZC(int(config['CZC']['delay'])), ))
        tsThread = threading.Thread(target = scraperThread, args = (TSBohemia(int(config['TSBohemia']['delay'])), ))

        alzaThread.daemon = True
        czcThread.daemon = True
        tsThread.daemon = True

        if config.getboolean('Alza', 'enabled'): alzaThread.start()
        if config.getboolean('CZC', 'enabled'): czcThread.start()
        if config.getboolean('TSBohemia', 'enabled'): tsThread.start()

        log(Severity.INFO, "Main", "Started!")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        log(Severity.FAIL, "Main", "Keyboard interrupt, exiting...")
        pass

    log(Severity.DEBUG, "Main", "-" * 16, "LOG END", "-" * 16)
