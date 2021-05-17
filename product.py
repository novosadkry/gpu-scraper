import jsons
import threading
import shortuuid

from redis import Redis

class Product():
    def __init__(self, store, uid, name, price, inStock, link):
        self.store = store
        self.id = uid
        self.name = name
        self.price = price
        self.inStock = inStock
        self.link = link

    def compare(self, other):
        if self.price != other.price: return False
        if self.inStock != other.inStock: return False
        return True

storedProducts = {}
redis = Redis(host = 'ip.zahrajto.wtf', port = 25543, password = 'tvojemama')
fetchLock = threading.Lock()

def hasProductChanged(product: Product):
    if product.id in storedProducts:
        sp = storedProducts[product.id]
        return not sp.compare(product)
    return True

def removeProduct(product: Product):
    storedProducts.pop(product.id, None)
    redis.delete(product.id)

def updateProduct(product: Product):
    if hasProductChanged(product):
        storedProducts[product.id] = product
        print(product.id, jsons.dumps(product))
        redis.set(product.id, jsons.dumps(product))

def onProductFetch(product: Product):
    with fetchLock:
        if product.inStock > 0: updateProduct(product)
        else: removeProduct(product)
