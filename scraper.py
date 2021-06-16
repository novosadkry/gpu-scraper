import time
import threading

from log import Severity
from log import logc

from product import ProductHandler
from config import config

class Scraper():
    def __init__(self, store, url, delay):
        self.store = store
        self.url = url
        self.delay = delay
        self.isReady = False

    def getDigitFromStock(self, stock) -> int:
        if stock is not None:
            for s in stock.split():
                if s.isdigit():
                    stock = int(s)
                    break
            else:
                stock = 0
        else:
            stock = 0
        return stock

    def setup(self):
        self.handler = ProductHandler(self.store)
        self.handler.setupRedis(
            host = config['Redis']['host'],
            port = int(config['Redis']['port']),
            password = config['Redis']['password']
        )
        self.isReady = True

    def start(self):
        if not self.isReady:
            self.setup()
        self.thread = threading.Thread(target = threadEntry, args = (self,))
        self.thread.daemon = True
        self.thread.isRunning = True
        self.thread.start()

    def stop(self):
        self.thread.isRunning = False

    def scrape(self):
        pass

def threadEntry(scraper: Scraper):
    logc(Severity.DEBUG, scraper.store, "Thread started!")
    t = threading.currentThread()
    while getattr(t, "isRunning", True):
        scraper.scrape()
        time.sleep(scraper.delay)
    logc(Severity.DEBUG, scraper.store, "Thread stopped!")
