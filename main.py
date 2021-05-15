from CZC import CZC
from product import Product

def onProduct(product: Product):
    print(product.name, product.price, product.inStock, sep=', ')

CZC().scrape(onProduct)