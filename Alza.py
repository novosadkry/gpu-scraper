from scraper import Scraper

import requests
import json
import time

from log import Severity
from log import logc

from product import Product
from bs4 import BeautifulSoup

def getDigitFromStock(stock) -> int:
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

class Alza(Scraper):
    def __init__(self, delay):
        Scraper.__init__(self, "Alza", "https://www.alza.cz", delay)

    def scrape(self, callback):
        pageNum = 1
        session = requests.session()

        urlPath = "/graficke-karty/18842862-p{pageNum}.htm"

        count = 0
        while (True):
            page = session.get(self.url + urlPath.format(pageNum = pageNum))

            soup = BeautifulSoup(page.content, 'html.parser')
            products = soup.find(id='boxes')

            if products is None:
                break

            products = products.findAll('div', class_='box')

            if len(products) < 1:
                break

            for product in products:
                meta = product.find('a', class_='name')

                uid = self.store + ":" + meta['data-impression-id']
                name = meta['data-impression-name']
                price = int(float(meta['data-impression-metric2'].replace(',', '.')))
                link = self.url + meta['href']

                stock = meta['data-impression-dimension13']
                stock = getDigitFromStock(stock)

                callback(Product(self.store, uid, name, price, stock, link))
                count += 1

            pageNum += 1
            time.sleep(self.delay)

        logc(Severity.INFO, self.store, f"Checked {count} products")
