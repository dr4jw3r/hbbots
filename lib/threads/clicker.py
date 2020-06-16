#====
from threading import Thread
from time import sleep, time
from lib.inputcontrol import click
from lib.utils.CancellationToken import CancellationToken
#====

class ClickerThread(object):
    def __init__(self, meat_type=None, singlescan=False, no_loot=False):
        self.cancellation_token = CancellationToken()
        
        self.thread = Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while not self.cancellation_token.is_cancelled:
            click()
            sleep(0.02)

    def stop(self):
        self.cancellation_token.cancel()