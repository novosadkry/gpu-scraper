import jsons
import requests
import threading

from log import Severity
from log import log

from redis import Redis
from config import config

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

postUrl = config['WebHost']['url'] + config['WebHost']['path']
postPass = config['WebHost']['pass']

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
    if product.id in storedProducts:
        storedProducts.pop(product.id, None)
        redis.delete(product.id)
        requests.post(postUrl, json={
            "type": "REMOVE",
            "id": product.id,
            "password": postPass})
        logProduct(Severity.REMOVE, product)

def updateProduct(product: Product):
    if hasProductChanged(product):
        storedProducts[product.id] = product
        redis.set(product.id, jsons.dumps(product))
        requests.post(postUrl, json={
            "type": "UPDATE",
            "id": product.id,
            "password": postPass})
        logProduct(Severity.UPDATE, product)

def onProductFetch(product: Product):
    with fetchLock:
        if product.inStock > 0: updateProduct(product)
        else: removeProduct(product)

def logProduct(severity: Severity, product: Product):
    log(severity, product.id, f"Name: '{product.name}', Price: {product.price}, InStock: {product.inStock}")