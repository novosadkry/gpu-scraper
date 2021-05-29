from product import ProductHandler
from config import config

class Scraper():
    def __init__(self, store, url, delay):
        self.store = store
        self.url = url
        self.delay = delay

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

    def scrape(self, callback):
        pass