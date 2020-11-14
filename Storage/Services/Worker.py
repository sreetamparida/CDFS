from pathlib import Path
import os
import subprocess
import sys


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

                


        