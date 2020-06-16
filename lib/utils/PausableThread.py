from time import sleep
from threading import Thread
# 
from lib.utils.CancellationToken import CancellationToken

class PausableThread(object):
    def __init__(self):
        self.cancellation_token = CancellationToken()
        self.is_started = False
        self.is_paused = False
        self.delay = 0
        self.thread = Thread(target=self.run, args=())
        self.thread.daemon = True        

    def pause(self):
        self.is_paused = True

    def resume(self, delay=0):
        self.delay = delay
        self.is_paused = False

    def start(self, delay=0):
        self.delay = delay
        if not self.is_started:
            self.thread.start()
            self.is_started = True
        else:
            self.resume()

    def startpaused(self):
        self.is_paused = True
        self.start()

    def stop(self):
        self.cancellation_token.cancel()

    def join(self):
        if self.is_started:
            self.thread.join()

    def run(self):
        if self.delay > 0:
            sleep(self.delay)