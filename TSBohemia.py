from scraper import Scraper

import requests
import jsons
import time
import re

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

class TSBohemia(Scraper):
    def __init__(self, delay):
        Scraper.__init__(self, "TSBohemia", "https://www.tsbohemia.cz", delay)

    def scrape(self, callback):
        pageNum = 1
        session = requests.session()

        urlPath = "/elektronika-a-it-pc-komponenty-graficke-karty_c5581.html?page={pageNum}"

        count = 0
        while (True):
            page = session.get(self.url + urlPath.format(pageNum = pageNum))

            soup = BeautifulSoup(page.content, 'html.parser')
            products = soup.find(id='gallarea')

            if products is None:
                break

            products = products.findAll('div', class_='prodbox')

            if len(products) < 1:
                break

            for product in products:
                uid = self.store + ":" + product['data-stiid']
                name = product.find('a', class_='stihref').text

                price = product.find('p', class_='wvat').text
                price = re.sub("[^\d]+", "", price)
                price = int(price)

                link = '/' + product.find('a', class_='stihref')['href']
                stock = product.find('em', class_='imgyes')
                stock = 0 if stock is None else getDigitFromStock(stock.text)

                callback(Product(self.store, uid, name, price, stock, link))
                count += 1

            pageNum += 1
            time.sleep(self.delay)

        logc(Severity.INFO, self.store, f"Checked {count} products")
