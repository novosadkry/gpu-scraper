class Scraper():
    def __init__(self, store, url, delay):
        self.store = store
        self.url = url
        self.delay = delay

    def scrape(self, callback):
        pass