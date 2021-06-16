from scraper import Scraper

import requests
import json
import time

from log import Severity
from log import logc

from product import Product
from bs4 import BeautifulSoup

class Alza(Scraper):
    def __init__(self, delay):
        Scraper.__init__(self, "Alza", "https://www.alza.cz", delay)

    def scrape(self):
        session = requests.session()

        urlPath = "/graficke-karty/18842862-p{pageNum}.htm"

        productCount = 0
        totalStock = 0
        pageNum = 1

        while (True):
            page = session.get(self.url + urlPath.format(pageNum = pageNum))

            soup = BeautifulSoup(page.content, 'html.parser')
            products = soup.find(id='boxes')

            if products is None:
                break

            products = products.findAll('div', class_='box')

            if len(products) < 1:
                break

            pageStock = 0
            for product in products:
                meta = product.find('a', class_='name')

                uid = self.store + ":" + meta['data-impression-id']
                name = meta['data-impression-name']
                price = int(float(meta['data-impression-metric2'].replace(',', '.')))
                link = self.url + meta['href']

                stock = meta['data-impression-dimension13']
                stock = self.getDigitFromStock(stock)

                if stock > 0:
                    self.handler.push(Product(self.store, uid, name, price, stock, link))
                    pageStock += 1

                productCount += 1

            if pageStock < 1:
                break

            pageNum += 1
            totalStock += pageStock

            time.sleep(self.delay)

        self.handler.flush()
        logc(Severity.INFO, self.store, f"Fetched {productCount} products ({totalStock} in stock) out of {pageNum} pages")
