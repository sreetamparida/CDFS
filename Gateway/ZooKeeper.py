from kazoo.client import KazooClient

class ZooKeeper:

    def __init__(self):
        self.client = KazooClient()
        self.client.start()

    def createZnode(self, node_id):
        path = '/cart/' + node_id
        self.client.ensure_path(path)

    def getValue(self, node_id):
        return self.client.get(node_id)[0].decode('utf-8')

    def setReplica(self, node_id, replica):
        path = '/cart/{node}/{replica}/'.format(node = node_id, replica = replica)
        self.client.ensure_path(path)

    def deleteReplica(self, node_id, replica):
        path = '/cart/{node}/{replica}/'.format(node = node_id, replica = replica)
        self.client.delete(path, recursive=True)
    
    def getReplica(self, node_id):
        path = '/cart/' + node_id
        return self.client.get_children(path)