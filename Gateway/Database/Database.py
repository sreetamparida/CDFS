import json

class Database:

    def __init__(self):
        self.DATABASE = None
        with open('Dependencies/data.json', 'r') as f:
            self.DATABASE = json.load(f)

        self.PRODUCTS = None
        self._mapProducts()

    def _mapProducts(self):
        self.PRODUCTS = {}
        for item in self.DATABASE:
            self.PRODUCTS[item['PRODUCT_NAME']] = int(item['ID']) -1 

    def getProductDetails(self, product_name):
        index = self.PRODUCTS[product_name]
        return self.DATABASE[index]