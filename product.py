import jsons
import threading
import shortuuid

from log import Severity
from log import log

from redis import Redis

class Product():
    def __init__(self, store, uid, name, price, inStock, link):
        self.store = store
        self.id = uid
        self.name = name
        self.price = price
        self.inStock = inStock
        self.link = link

    @staticmethod
    def fromJSON(s):
        d = jsons.loads(s)
        return Product(
            d['store'],
            d['id'],
            d['name'],
            d['price'],
            d['inStock'],
            d['link']
        )

    def compare(self, other):
        if self.price != other.price: return False
        if self.inStock != other.inStock: return False
        return True

redis = None
storedProducts = {}
fetchLock = threading.Lock()

def setupRedis(**kwargs):
    global redis
    redis = Redis(**kwargs)
    loadProducts()

def loadProducts():
    count = 0
    for key in redis.scan_iter("*"):
        product = Product.fromJSON(redis.get(key))
        storedProducts[product.id] = product
        count += 1
    log(Severity.INFO, "Redis", f"Loaded {count} products")

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
        log(Severity.UPDATE, product.id, f"[name: {product.name}, price: {product.price}, inStock: {product.inStock}]")
        redis.set(product.id, jsons.dumps(product))

def onProductFetch(product: Product):
    with fetchLock:
        if product.inStock > 0: updateProduct(product)
        else: removeProduct(product)
