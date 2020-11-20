import os
from pathlib import Path
import subprocess
class Quorum:

    def __init__(self):
        self.HOME = Path.home()
        self.DFS_HOME = os.path.join(self.HOME, '.dfs')
        if not os.path.exists(self.DFS_HOME):
            try:
                cmd = subprocess.run('mkdir ' + self.DFS_HOME, shell = True, check = True)
                if cmd.returncode == 0:
                    print('*** Default Directory Created')
            except subprocess.CalledProcessError as e:
                print(e.stderr)
        self.DFS_CART = os.path.join(self.DFS_HOME, 'cart')
        self.DFS_QUORUM = os.path.join(self.DFS_HOME, 'quorum')
        if not os.path.exists(self.DFS_QUORUM):
            try:
                cmd = subprocess.run('mkdir ' + self.DFS_QUORUM, shell = True, check = True)
                if cmd.returncode == 0:
                    print('*** Quorum Directory Created')
            except subprocess.CalledProcessError as e:
                print(e.stderr)

    def implementQuorum(self, updatedNodeIP, outdatedNodeIP, cart_id):
        getUpdated = 'scp -r root@{updatedNodeIP}:{dfsDirectory}/{cart_id} {quorumPath}'.format(
            updatedNodeIP = updatedNodeIP,
            dfsDirectory = self.DFS_CART,
            cart_id = cart_id,
            quorumPath = self.DFS_QUORUM
        )

        sendUpdated = 'scp -r {quorumPath}/{cartID} root@{outdatedNodeIP}:{dfsDirectory}/'.format(
            quorumPath = self.DFS_QUORUM,
            cartID = cart_id,
            outdatedNodeIP = outdatedNodeIP,
            dfsDirectory = self.DFS_CART,
            cart_id = cart_id
        )
        
        subprocess.run(getUpdated,  shell = True, check = True)
        subprocess.run(sendUpdated, shell = True, check = True)

# if __name__ == "__main__":
#     q = Quorum()
#     q.implementQuorum('10.0.3.147', '10.0.3.198', 'ce4568ed')