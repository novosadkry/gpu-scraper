from CZC import CZC
from Alza import Alza
from product import Product

import jsons

storedProducts = {}

def onProductUpdated(product: Product):
    print(jsons.dumps(storedProducts[product.name]))


def addNewProduct(product: Product):
    storedProducts[product.name] = {
        product.store: {
            "price": product.price,
            "inStock": product.inStock
        }
    }


def updateProduct(product: Product):
    updated = False

    if product.store not in storedProducts[product.name]:
        updated = True
    else:
        if storedProducts[product.name][product.store]["price"] != product.price:
            updated = True
        if storedProducts[product.name][product.store]["inStock"] != product.inStock:
            updated = True

    storedProducts[product.name][product.store] = {
        "price": product.price,
        "inStock": product.inStock
    }

    if updated:
        onProductUpdated(product)


def onProductFetch(product: Product):
    if product.inStock == 0:
        return

    if product.name in storedProducts:
        updateProduct(product)
    else:
        addNewProduct(product)


Alza().scrape(onProductFetch)
CZC().scrape(onProductFetch)