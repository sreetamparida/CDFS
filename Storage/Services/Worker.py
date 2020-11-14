from pathlib import Path
import os
import subprocess
import sys
import json


class Worker:

    def __init__(self):
        self.HOME = Path.home()
        self.DFS_HOME = os.path.join(self.HOME, '.dfs')
        self.DFS_CART = os.path.join(self.DFS_HOME, 'cart')
        self.DFS_ATTRIB = os.path.join(self.DFS_HOME, 'attrib')

        if not os.path.exists(self.DFS_HOME):
            try:
                cmd = subprocess.run('mkdir ' + self.DFS_HOME, shell = True, check = True)
                if cmd.returncode == 0:
                    print('*** Default Directory Created')
            except subprocess.CalledProcessError as e:
                print(e.stderr)

        if not os.path.exists(self.DFS_CART):
            try:
                cmd = subprocess.run('mkdir ' + self.DFS_CART, shell = True, check = True)
                if cmd.returncode == 0:
                    print('*** Cart Directory Created')
            except subprocess.CalledProcessError as e:
                print(e.stderr)

        if not os.path.exists(self.DFS_ATTRIB):
            try:
                cmd = subprocess.run('mkdir ' + self.DFS_ATTRIB, shell = True, check = True)
                if cmd.returncode == 0:
                    print('*** Attribute Directory Created')
            except subprocess.CalledProcessError as e:
                print(e.stderr)
        
    def createCart(self, UID):
        cart = os.path.join(self.DFS_CART, UID)
        if not os.path.exists(cart):
            try:
                cmd = subprocess.run('mkdir ' + cart, shell = True, check = True)
                if cmd.returncode == 0:
                    print('*** Cart Created')
            except subprocess.CalledProcessError as e:
                print(e.stderr)
        cart = open(os.path.join(cart, 'cart.json'), 'x')
        cart.close()
        meta = open(os.path.join(cart, 'metadata'), 'x')
        meta.close()

    def addToCart(self, UID, value):
        path = UID + '/cart.json'
        path = os.path.join(self.DFS_CART, path)

        with open(path, 'r+') as f:
            cart = json.load(f)
            cart.append(value)
            f.seek(0)
            json.dump(cart,f)
    
    def deleteFromCart(self, UID, value):
        path = UID + '/cart.json'
        path = os.path.join(self.DFS_CART, path)

        with open(path, 'r+') as f:
            cart = json.load(f)
            for item in cart:
                if item['ID'] == value['ID']:
                    cart.remove(item)
            f.seek(0)
            json.dump(cart,f)

    def updateCart(self, UID, value):
        path = UID + '/cart.json'
        path = os.path.join(self.DFS_CART, path)

        with open(path, 'r+') as f:
            cart = json.load(f)
            for item in cart:
                if item['ID'] == value['ID']:
                    cart.remove(item)
                    cart.append(value)
            f.seek(0)
            json.dump(cart,f)
    
    def listCart(self, UID, value):
        path = UID + '/cart.json'
        path = os.path.join(self.DFS_CART, path)

        with open(path, 'r') as f:
            cart = json.load(f)
        
        return cart


        
    
        
        


        







        