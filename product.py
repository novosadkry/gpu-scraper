import jsons
import requests
import threading

from log import Severity
from log import logc

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
        if self.id != other.id: return False
        if self.price != other.price: return False
        if self.inStock != other.inStock: return False
        return True

    def __eq__(self, value):
        return self.compare(value) if isinstance(value, Product) else False

    def __hash__(self):
        return hash(self.id + str(self.price) + str(self.inStock))

postUrl = config['WebHost']['url'] + config['WebHost']['path']
postPass = config['WebHost']['pass']

class ProductHandler():
    def __init__(self, store):
        self.store = store
        self.storedProducts = set()
        self.newBatch = True
        self.buffer = set()

    def setupRedis(self, **kwargs):
        self.redis = Redis(**kwargs)
        # TODO: Flush DB on start
        self.__loadProducts()

    def __loadProducts(self):
        for key in self.redis.scan_iter(f"{self.store}:*"):
            product = Product.fromJSON(self.redis.get(key))
            self.storedProducts.add(product)
        logc(Severity.INFO, self.store, f"Loaded {len(self.storedProducts)} products")

    def push(self, product: Product):
        if self.newBatch:
            self.buffer.clear()
        self.buffer.add(product)
        self.newBatch = False

    def flush(self):
        newProducts = self.buffer - self.storedProducts
        removedProducts = self.storedProducts - self.buffer

        for product in newProducts:
            self.redis.set(product.id, jsons.dumps(product))
            logProduct(Severity.UPDATE, product)

        for product in removedProducts:
            self.redis.delete(product.id, jsons.dumps(product))
            logProduct(Severity.REMOVE, product)

        # requests.post(postUrl, json={
        #     "type": "UPDATE",
        #     "password": postPass})

        self.storedProducts = self.buffer
        self.newBatch = True

def logProduct(severity: Severity, product: Product):
    logc(severity, product.id, f"Name: '{product.name}', Price: {product.price}, InStock: {product.inStock}")
