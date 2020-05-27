from time import sleep
from threading import Thread

from lib.threads.equipitem import EquipItemThread

class MpRegenThread(object):
    def __init__(self, shield):
        self.shield = shield
        self.keeprunning = True

        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while self.keeprunning:
            EquipItemThread(self.shield)
            sleep(20)

    def stop(self):
        self.keeprunning = False
        pass