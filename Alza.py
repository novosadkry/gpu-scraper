from scraper import Scraper

import requests
import json
import time
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
    def __init__(self):
        Scraper.__init__(self, "Alza", "https://www.alza.cz/graficke-karty/18842862-p{pageNum}.htm")

    def scrape(self, callback):
        pageNum = 1
        session = requests.session()

        while (True):
            page = session.get(self.url.format(pageNum = pageNum))

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

                stock = meta['data-impression-dimension13']
                stock = getDigitFromStock(stock)

                callback(Product(self.store, uid, name, price, stock))

            pageNum += 1
            time.sleep(1)
