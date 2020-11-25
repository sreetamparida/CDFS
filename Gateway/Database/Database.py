import json
import requests

class Database:

    def __init__(self):
        self.DATABASE = None
        self.USERDATA = None
        self.PRODUCTS = None

    def _mapProducts(self):
        self.PRODUCTS = {}
        for item in self.DATABASE:
            self.PRODUCTS[item['PRODUCT_NAME'].upper()] = int(item['ID']) -1 

    def getProductDetails(self, ip,  product_name):
        url = 'http://{ip}:5000/product'.format(ip=ip)
        self.DATABASE = requests.post(url)
        self._mapProducts()
        index = self.PRODUCTS[product_name]
        return self.DATABASE[index]
    
    def getUID(self, ip, username):
        url = 'http://{ip}:5000/user'.format(ip=ip)
        self.USERDATA = requests.post(url)
        if username in self.USERDATA:
            return self.USERDATA[username]
        else:
            return 'NOT A USER'