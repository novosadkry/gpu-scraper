import time

from CZC import CZC
from Alza import Alza
from TSBohemia import TSBohemia

from scraper import Scraper

from log import Severity
from log import log
from log import logc

from config import config

class App:
    def start(self):
        log(Severity.DEBUG, "Main", "-" * 15, "LOG BEGIN", "-" * 15)
        log(Severity.INFO, "Main", "Starting...")

        self.isRunning = True

        self.alzaScraper = Alza(int(config['Alza']['delay']))
        self.czcScraper = CZC(int(config['CZC']['delay']))
        self.tsScraper = TSBohemia(int(config['TSBohemia']['delay']))

        if config.getboolean('Alza', 'enabled'): self.alzaScraper.start()
        if config.getboolean('CZC', 'enabled'): self.czcScraper.start()
        if config.getboolean('TSBohemia', 'enabled'): self.tsScraper.start()

        log(Severity.INFO, "Main", "Started!")

        while self.isRunning:
            time.sleep(1)

    def stop(self):
        log(Severity.FAIL, "Main", "Exiting...")

        self.isRunning = False

        self.alzaScraper.stop()
        self.czcScraper.stop()
        self.tsScraper.stop()

        self.alzaScraper.thread.join()
        self.czcScraper.thread.join()
        self.tsScraper.thread.join()

        log(Severity.DEBUG, "Main", "-" * 16, "LOG END", "-" * 16)