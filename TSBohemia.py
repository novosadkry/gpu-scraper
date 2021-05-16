from scraper import Scraper

import requests
import jsons
import time
import re

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

class TSBohemia(Scraper):
    def __init__(self):
        Scraper.__init__(self, "TSBohemia", "https://www.tsbohemia.cz/elektronika-a-it-pc-komponenty-graficke-karty_c5581.html?page={pageNum}")

    def scrape(self, callback):
        pageNum = 1
        session = requests.session()

        while (True):
            page = session.get(self.url.format(pageNum = pageNum))

            soup = BeautifulSoup(page.content, 'html.parser')
            products = soup.find(id='gallarea')

            if products is None:
                break

            products = products.findAll('div', class_='prodbox')

            if len(products) < 1:
                break

            for product in products:
                name = product.find('a', class_='stihref').text

                price = product.find('p', class_='wvat').text
                price = re.sub("[^\d]+", "", price)
                price = int(price)

                stock = product.find('em', class_='imgyes')

                if stock is None:
                    stock = 0
                else:
                    stock = getDigitFromStock(stock.text)

                callback(Product(self.store, name, price, stock))

            pageNum += 1
            time.sleep(1)
