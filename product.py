import jsons
import threading
import redis
import shortuuid

class Product():
    def __init__(self, store, name, price, inStock):
        self.store = store
        self.name = name
        self.price = price
        self.inStock = inStock


class ProductGroup():
    def __init__(self, uid, name):
        self.uid = uid
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
        return jsons.dumps({"id": self.uid, "stores": data})


redisInst = redis.Redis(host = 'ip.zahrajto.wtf', port = 25543, password = 'tvojemama')
redisInst.flushdb()

storedGroups = {}
fetchLock = threading.Lock()


def pushGroupToRedis(group: ProductGroup):
    redisInst.set(group.name, group.toJSON())


def removeGroupFromRedis(group: ProductGroup):
    redisInst.delete(group.name)


def onProductUpdated(product: Product):
    pushGroupToRedis(storedGroups[product.name])
    print(product.name + " : " + storedGroups[product.name].toJSON())


def removeGroup(group: ProductGroup):
    storedGroups.pop(group.name, None)
    removeGroupFromRedis(group)


def removeProduct(product: Product):
    if product.name in storedGroups:
        group = storedGroups[product.name]
        group.remove(product)

        pushGroupToRedis(storedGroups[product.name])

        if len(group.products) < 1:
            removeGroup(group)


def getOrAddGroup(product: Product):
    if product.name not in storedGroups:
        storedGroups[product.name] = ProductGroup(shortuuid.uuid(), product.name)
    return storedGroups[product.name]


def addProduct(product: Product):
    group = getOrAddGroup(product)
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
