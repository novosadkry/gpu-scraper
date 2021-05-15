from scraper import Scraper

import requests
import json
import time
from product import Product
from bs4 import BeautifulSoup

def getDigitFromStock(stock) -> int:
    if stock is not None:
        for s in stock.text.split():
            if s.isdigit():
                stock = int(s)
                break
        else:
            stock = 0
    else:
        stock = 0
    return stock

class CZC(Scraper):
    def __init__(self):
        Scraper.__init__(self, "https://www.czc.cz/graficke-karty/produkty")

    def scrape(self, callback):
        toSkip = 0

        while (True):
            params = f'?q-first={toSkip}'
            page = requests.get(self.url + params)

            soup = BeautifulSoup(page.content, 'html.parser')
            products = soup.find(id='tiles')

            if products is None:
                break

            products = products.findAll('div', class_='new-tile')

            for product in products:
                meta = json.loads(product['data-ga-impression'])

                stock = product.find('span', class_='availability-state-on-stock')
                stock = getDigitFromStock(stock)

                callback(Product(meta['name'], meta['price'], stock))

            toSkip += len(products)
            time.sleep(1)
