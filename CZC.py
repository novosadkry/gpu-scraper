from scraper import Scraper

import requests
import json
import time

from log import Severity
from log import logc

from product import Product
from bs4 import BeautifulSoup

class CZC(Scraper):
    def __init__(self, delay):
        Scraper.__init__(self, "CZC", "https://www.czc.cz", delay)

    def scrape(self):
        toSkip = 0
        session = requests.session()

        urlParams = '?q-first={toSkip}'
        urlPath = "/graficke-karty/produkty"

        totalStock = 0
        pageCount = 0
        productCount = 0

        while (True):
            page = session.get(self.url + urlPath + urlParams.format(toSkip = toSkip))

            soup = BeautifulSoup(page.content, 'html.parser')
            products = soup.find(id='tiles')

            if products is None:
                break

            products = products.findAll('div', class_='new-tile')

            pageStock = 0
            for product in products:
                meta = json.loads(product['data-ga-impression'])

                uid = self.store + ":" + meta['id']
                name = meta['name']
                price = meta['price']

                link = product.find('a', class_='tile-link')['href']
                link = self.url + link

                stock = product.find('span', class_='availability-state-on-stock')
                stock = 0 if stock is None else self.getDigitFromStock(stock.text)

                if stock > 0:
                    self.handler.push(Product(self.store, uid, name, price, stock, link))
                    pageStock += 1

                productCount += 1

            if pageStock < 1:
                break

            pageCount += 1
            totalStock += pageStock
            toSkip += len(products)

            time.sleep(self.delay)

        self.handler.flush()
        logc(Severity.INFO, self.store, f"Fetched {productCount} products ({totalStock} in stock) out of {pageCount} pages")
