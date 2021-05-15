from CZC import CZC
from Alza import Alza
from product import Product

import json

products = {}

def onProductFetch(product: Product):
    print(product.name, product.price, product.inStock, sep=', ')
    products[product.name] = product

Alza().scrape(onProductFetch)
CZC().scrape(onProductFetch)