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

class Alza(Scraper):
    def __init__(self):
        Scraper.__init__(self, "https://www.alza.cz/graficke-karty/18842862.htm")

    def scrape(self, callback):
        page = 0

        while (True):
            params = f'#f&pg={page}'
            page = requests.get(self.url + params)

            soup = BeautifulSoup(page.content, 'html.parser')
            products = soup.find(id='boxes')

            if products is None:
                break

            products = products.findAll('div', class_='box')

            for product in products:
                name = product.find('a', class_='name').text
                price = product.find('span', class_='c2').text

                stock = product.find('a', 'impression-binded')['data-impression-dimension13']
                stock = getDigitFromStock(stock)

                callback(Product(name, price, stock))

            page += 1
            time.sleep(1)
