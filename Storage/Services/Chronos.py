from threading import Timer

class Chronos:

    def __init__(self):
        self.manager = None
        self.isRunning = False
        self.interval = 10

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

    def _chronos(self):
        pass