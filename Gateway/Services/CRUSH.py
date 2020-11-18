#pylint: disable=too-many-function-args
import hashlib

class CRUSH:

    def __init__(self, replications, cluster_size):
        self.PRIME = 1190611
        self.hash = hashlib.shake_128()
        self.REPLICATIONS = replications
        self.CLUSTER_SIZE = cluster_size

    def _crush(self, username, replica_number, cluster_size, fail_count=0, first_n = 1):
        replica_number = replica_number + fail_count * first_n
        self.hash.update(bytes(username, 'utf-8'))
        hashValue = int(self.hash.hexdigest(8), base=16)
        nodeNumber = (hashValue + replica_number * self.PRIME) % cluster_size
        return nodeNumber

    def select(self, username, reselect = False, data=None):
        if not reselect:
            nodes = []
            for replica in range(1,self.REPLICATIONS+1):
                nodes.append(self._crush(username, replica, self.CLUSTER_SIZE))
            return nodes
        else:
            if data['fail_count'] < self.REPLICATIONS:
                return self._crush(username, data['replication_number'], self.CLUSTER_SIZE, data['fail_count'])
            else:
                return self._crush(username, data['replication_number'], self.CLUSTER_SIZE, data['fail_count'], self.REPLICATIONS)

    def getHash(self, value):
        self.hash.update(bytes(value, 'utf-8'))
        return self.hash.hexdigest(8)

