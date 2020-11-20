import json

class Database:

    def __init__(self):
        self.DATABASE = None
        with open('Database/Dependencies/data.json', 'r') as f:
            self.DATABASE = json.load(f)

        self.USERDATA = None
        with open('Database/Dependencies/userdata.json', 'r') as f:
            self.USERDATA = json.load(f)

        self.PRODUCTS = None
        self._mapProducts()

    def _mapProducts(self):
        self.PRODUCTS = {}
        for item in self.DATABASE:
            self.PRODUCTS[item['PRODUCT_NAME'].upper()] = int(item['ID']) -1 

    def getProductDetails(self, product_name):
        index = self.PRODUCTS[product_name]
        return self.DATABASE[index]
    
    def getUID(self, username):
        if username in self.USERDATA:
            return self.USERDATA[username]
        else:
            return 'NOT A USER'