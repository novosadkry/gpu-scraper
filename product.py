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

redis = Redis(host = 'ip.zahrajto.wtf', port = 25543, password = 'tvojemama')
fetchLock = threading.Lock()

def removeProduct(product: Product):
    redis.delete(product.id)

def updateProduct(product: Product):
    print(product.id, jsons.dumps(product))
    redis.set(product.id, jsons.dumps(product))

def onProductFetch(product: Product):
    with fetchLock:
        if product.inStock > 0:
            updateProduct(product)
        else:
            removeProduct(product)
