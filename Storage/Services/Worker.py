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
        self.DFS_HANDOFF = os.path.join(self.DFS_HOME, 'handoff')
        self.SECONDARY_INDEX_PATH = os.path.join(self.DFS_ATTRIB, 'secondaryindex.json')

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

        if not os.path.exists(self.DFS_HANDOFF):
            try:
                cmd = subprocess.run('mkdir ' + self.DFS_HANDOFF, shell = True, check = True)
                if cmd.returncode == 0:
                    print('*** Handoff Directory Created')
                    handoff_path = os.path.join(self.DFS_HANDOFF, '/handoff.json')
                    handoff = open(handoff_path, 'x')
                    handoff.write([])
                    handoff.close()
            except subprocess.CalledProcessError as e:
                print(e.stderr)

        if not os.path.exists(self.DFS_ATTRIB):
            try:
                cmd = subprocess.run('mkdir ' + self.DFS_ATTRIB, shell = True, check = True)
                if cmd.returncode == 0:
                    print('*** Attribute Directory Created')
                    secondaryIndex = open(self.SECONDARY_INDEX_PATH, 'x')
                    secondaryIndex.write('{}')
                    secondaryIndex.close()
            except subprocess.CalledProcessError as e:
                print(e.stderr)
        
    def createCart(self, UID):
        path = os.path.join(self.DFS_CART, UID)
        if not os.path.exists(path):
            try:
                cmd = subprocess.run('mkdir ' + path, shell = True, check = True)
                if cmd.returncode == 0:
                    print('*** Cart Created')
            except subprocess.CalledProcessError as e:
                print(e.stderr)
        cart = open(os.path.join(path, 'cart.json'), 'x')
        cart.write('[]')
        cart.close()
        meta = open(os.path.join(path, 'metadata.json'), 'x')
        meta.write('{"VERSION":1, "TIMESTAMP":123456}')
        meta.close()

    def addToCart(self, UID, value):
        path = UID + '/cart.json'
        path = os.path.join(self.DFS_CART, path)

        with open(path, 'r+') as f:
            cart = json.load(f)
            cart.append(value)
            f.seek(0)
            f.truncate()
            json.dump(cart,f)
    
    def deleteFromCart(self, UID, value):
        path = UID + '/cart.json'
        path = os.path.join(self.DFS_CART, path)

        with open(path, 'r+') as f:
            cart = json.load(f)
            for item in cart:
                if item['ID'] == value['ID']:
                    cart.remove(item)
                    break
            f.seek(0)
            f.truncate()
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
                    break
            f.seek(0)
            f.truncate()
            json.dump(cart,f)
    
    def listCart(self, UID):
        cart_path = UID + '/cart.json'
        cart_path = os.path.join(self.DFS_CART, cart_path)
        meta_path = UID + '/metadata.json'
        meta_path = os.path.join(self.DFS_CART, meta_path)

        with open(meta_path, 'r') as f:
            meta = json.load(f)

        with open(cart_path, 'r') as f:
            cart = json.load(f)
        
        result = {
            'CART': cart,
            'METADATA': meta
        }
        
        return result

    def updateSecondaryIndex(self, UID, ATTRIB_ID, delete=False):
        with open(self.SECONDARY_INDEX_PATH, 'r+') as f:
            secondaryIndex = json.load(f)
            if not delete:
                if ATTRIB_ID not in secondaryIndex:
                    secondaryIndex[ATTRIB_ID] = []
                secondaryIndex[ATTRIB_ID].append(UID)
                f.seek(0)
                f.truncate()
                json.dump(secondaryIndex, f)
            else:
                if ATTRIB_ID in secondaryIndex:
                    if UID in secondaryIndex[ATTRIB_ID]:
                        secondaryIndex[ATTRIB_ID].remove(UID)
                        f.seek(0)
                        f.truncate()
                        json.dump(secondaryIndex,f)

    def getSecondaryIndex(self, ATTRIB_ID):
        with open(self.SECONDARY_INDEX_PATH, 'r') as f:
            indexes = json.load(f)

        if ATTRIB_ID in indexes:
            return indexes[ATTRIB_ID]
        else:
            return []

    def updateMetadata(self, UID, version, timestamp):
        path = UID + '/metadata.json'
        path = os.path.join(self.DFS_CART, path)

        with open(path, 'r+') as f:
            meta = json.load(f)
            meta['VERSION'] = version
            meta['TIMESTAMP'] = timestamp
            f.seek(0)
            f.truncate()
            json.dump(meta, f)

    def getMetadata(self, UID):
        path = UID + '/metadata.json'
        path = os.path.join(self.DFS_CART, path)

        with open(path, 'r') as f:
            meta = json.load(f)
            return meta

    def handleHandoff(self, instruction):
        path = os.path.join(self.DFS_HANDOFF, '/handoff.json')
        with open(path, 'r+') as f:
            handoffInstruction = json.load(f)
            handoffInstruction.append(instruction)
            f.seek(0)
            f.truncate()
            json.dump(handoffInstruction, f)
        

    

    
    