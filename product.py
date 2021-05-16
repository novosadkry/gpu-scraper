import jsons
import threading
import redis

class Product():
    def __init__(self, store, name, price, inStock):
        self.store = store
        self.name = name
        self.price = price
        self.inStock = inStock

class ProductGroup():
    def __init__(self, name):
        self.name = name
        self.products = []

    def remove(self, product: Product):
        self.products = [p for p in self.products if p.store != product.store]

    def add(self, product: Product):
        for p in self.products:
            if p.store == product.store:
                p.price = product.price
                p.inStock = product.inStock
                break
        else:
            self.products.append(product)

    def contains(self, product: Product):
        for p in self.products:
            if p.store == product.store:
                return True
        return False

    def hasChanged(self, product: Product):
        for p in self.products:
            if p.store == product.store:
                if p.inStock != product.inStock: return True
                if p.price != product.price: return True
        return False

    def toJSON(self):
        data = []
        for p in self.products:
            data.append({"store": p.store, "price": p.price, "inStock": p.inStock})
        return jsons.dumps(data)


redisInst = redis.Redis(host = 'ip.zahrajto.wtf', port = 25543, password = 'tvojemama')
redisInst.flushdb()

def pushGroupToRedis(group: ProductGroup):
    redisInst.set(group.name, group.toJSON())

def removeGroupFromRedis(group: ProductGroup):
    redisInst.delete(group.name)


storedGroups = {}
fetchLock = threading.Lock()

def onProductUpdated(product: Product):
    pushGroupToRedis(storedGroups[product.name])
    print(product.name + " : " +storedGroups[product.name].toJSON())

def onProductRemoved(product: Product):
    pushGroupToRedis(storedGroups[product.name])

def onGroupRemoved(group: ProductGroup):
    removeGroupFromRedis(group)


def removeGroup(group: ProductGroup):
    storedGroups.pop(group.name, None)
    onGroupRemoved(group)

def removeProduct(product: Product):
    if product.name in storedGroups:
        group = storedGroups[product.name]
        group.remove(product)
        onProductRemoved(product)

        if len(group.products) < 1:
            removeGroup(group)

def addProduct(product: Product):
    if product.name not in storedGroups:
        newGroup = ProductGroup(product.name)
        newGroup.add(product)
        storedGroups[product.name] = newGroup
    else:
        group = storedGroups[product.name]
        group.add(product)

def updateProduct(product: Product):
    notifyUpdate = True

    if product.name in storedGroups:
        group = storedGroups[product.name]
        if group.contains(product):
            notifyUpdate = group.hasChanged(product)

    addProduct(product)

    if notifyUpdate:
        onProductUpdated(product)

def onProductFetch(product: Product):
    with fetchLock:
        if product.inStock > 0:
            updateProduct(product)
        else:
            removeProduct(product)
