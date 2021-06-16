from CZC import CZC
from Alza import Alza
from TSBohemia import TSBohemia

from scraper import Scraper

from log import Severity
from log import log
from log import logc

from config import config

import time

# TODO: Timestamp k datům (pro filtr "Nové")

if __name__ == '__main__':
    try:
        log(Severity.DEBUG, "Main", "-" * 15, "LOG BEGIN", "-" * 15)
        log(Severity.INFO, "Main", "Starting up...")

        alzaScraper = Alza(int(config['Alza']['delay']))
        czcScraper = CZC(int(config['CZC']['delay']))
        tsScraper = TSBohemia(int(config['TSBohemia']['delay']))

        if config.getboolean('Alza', 'enabled'): alzaScraper.start()
        if config.getboolean('CZC', 'enabled'): czcScraper.start()
        if config.getboolean('TSBohemia', 'enabled'): tsScraper.start()

        log(Severity.INFO, "Main", "Started!")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        log(Severity.FAIL, "Main", "Keyboard interrupt, exiting...")

        alzaScraper.stop()
        czcScraper.stop()
        tsScraper.stop()

        alzaScraper.thread.join()
        czcScraper.thread.join()
        tsScraper.thread.join()

    log(Severity.DEBUG, "Main", "-" * 16, "LOG END", "-" * 16)
