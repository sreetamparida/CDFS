from threading import Timer
import requests
import json
from pathlib import Path
import os

class Chronos:

    def __init__(self):
        self.manager = None
        self.isRunning = False
        self.interval = 10
        self.HOME = Path.home()
        self.DFS_HOME = os.path.join(self.HOME, '.dfs')
        self.DFS_HANDOFF_FILE = os.path.join(self.DFS_HOME, 'handoff/handoff.json')

    def _run(self):
        self.isRunning = False
        self.start()
        self._chronos()

    def start(self):
        if not self.isRunning:
            self.manager = Timer(self.interval, self._run)
            self.manager.start()
            self.isRunning = True

    def stop(self):
        print('*** STOPPING CHRONOS')
        self.manager.cancel()
        self.isRunning = False
    
    def _executeQuery(self, COMMAND, ip, data):
        url = 'http://{ip}:5000/'.format(ip=ip)

        if COMMAND == 'ADD':
            url = url + 'addtocart'
            req = requests.post(url, data=data)
            if req.status_code == 200:
                return req.json()
            else:
                return 'FAIL'

        elif COMMAND == 'DELETE':
            url = url + 'deletefromcart'
            req = requests.post(url, data=data)
            if req.status_code == 200:
                return req.json()
            else:
                return 'FAIL'
        
        elif COMMAND == 'UPDATE':
            url = url + 'updatecart'
            req = requests.post(url, data=data)
            if req.status_code == 200:
                return req.json()
            else:
                return 'FAIL'

    def _chronos(self):

        instructions = []
        completed = []
        with open(self.DFS_HANDOFF_FILE, 'r+') as f:
            instructions = json.load(f)
            if len(instructions) > 0:
                for instruction in instructions:
                    res = self._executeQuery(instruction['COMMAND'], instruction['IP'], instruction['DATA'])
                    if res != 'FAIL':
                        completed.append(instruction)
                for instruction in completed:
                    instructions.remove(instruction)
                json.dump(instructions, f)