from kazoo.client import KazooClient

class ZooKeeper:

    def __init__(self):
        self.client = KazooClient()
        self.client.start()
        self.cleanup()

    def createCart(self, cart_id):
        path = '/cart/' + cart_id
        self.client.ensure_path(path)

    def setReplica(self, cart_id, replica):
        path = '/cart/{node}/{replica}/'.format(node = cart_id, replica = replica)
        self.client.ensure_path(path)

    def deleteReplica(self, cart_id, replica):
        path = '/cart/{node}/{replica}/'.format(node = cart_id, replica = replica)
        self.client.delete(path, recursive=True)
    
    def getReplica(self, cart_id):
        path = '/cart/' + cart_id
        return self.client.get_children(path)
    
    def getCarts(self):
        return self.client.get_children('/cart/')

    def getNodes(self):
        return self.client.get_children('/node/')
        
    def getNodeIP(self, node_id):
        path = '/node/' + node_id
        return self.client.get(path)[0].decode('utf-8')
    
    def getHandoffNodeIP(self, node_id):
        path = '/handoff/' + node_id
        return self.client.get(path)[0].decode('utf-8')

    def updateSecondaryIndex(self, attrib_id, cart_id, delete=False):
        path = '/secondaryindex/{attrib_id}/{cart_id}'.format(attrib_id=attrib_id, cart_id=cart_id)
        if not delete:
            self.client.ensure_path(path)
        else:
            self.client.delete(path)

    def getSecondaryList(self, attrib_id):
        path = '/secondaryindex/{attrib_id}'.format(attrib_id=attrib_id)
        return self.client.get_children(path)
    
    def exists(self, cart_id):
        carts = self.getCarts()
        if cart_id in carts:
            return True
        else:
            return False

    def cleanup(self):
        self.client.delete('/cart/', recursive=True)
        self.client.delete('/secondaryindex/', recursive=True)
        self.client.ensure_path('/cart/')
        self.client.ensure_path('/secondaryindex/')