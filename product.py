import jsons
import threading
import redis

class Product():
    def __init__(self, store, name, price, inStock):
        self.store = store
        self.name = name
        self.price = price
        self.inStock = inStock


storedProducts = {}
fetchLock = threading.Lock()
redisInst = redis.Redis(host = 'ip.zahrajto.wtf', port = 25543, password = 'tvojemama')


def pushStoredToRedis(product: Product):
    redisInst.set(product.name, jsons.dumps(storedProducts[product.name]))


def onProductUpdated(product: Product):
    print(product.name + " : " + jsons.dumps(storedProducts[product.name]))


def addNewProduct(product: Product):
    storedProducts[product.name] = {
        product.store: {
            "price": product.price,
            "inStock": product.inStock
        }
    }
    pushStoredToRedis(product)


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
        pushStoredToRedis(product)
        onProductUpdated(product)


def onProductFetch(product: Product):
    if product.inStock == 0:
        return

    with fetchLock:
        if product.name in storedProducts:
            updateProduct(product)
        else:
            addNewProduct(product)