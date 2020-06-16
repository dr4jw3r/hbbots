import time

from threading import Thread
from random import randint

from lib.inputcontrol import *

from lib.threads.CastSpellThread import CastSpellThread

class FakeAmpThread(object):
    def __init__(self):
        self.keeprunning = True
        self.selfamptime = None

        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while self.keeprunning:
            if self.selfamptime is None:
                CastSpellThread("amp")
                moveto((400, 280))
                sleep(2)
                click()
                self.selfamptime = time.time()
            elif time.time() - self.selfamptime >= 60:
                self.selfamptime = None
            else:
                delay = randint(0, 3)
                CastSpellThread("amp")
                sleep(2)
                sleep(delay)
                rightdown()
                sleep(0.05)
                rightup()


    def stop(self):
        self.keeprunning = False