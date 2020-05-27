from time import sleep
from threading import Thread

from lib.inputcontrol import *
from lib.imagesearch import imagesearch_loop

class AlchemyThread(object):
    def __init__(self, positions):
        self.stopthread = False
        self.positions = positions

        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def make(self):
        pos = imagesearch_loop("./common/samples/alch/trynow2.png", 0.1, 0.5)
        moveto(pos, 10)
        click()
        sleep(3)

    def run(self):
        while self.stopthread == False:
            for position in self.positions:
                if position is not None:
                    moveto(position)
                    click(2, 0.05)

            self.make()
    
    def stop(self):
        self.stopthread = True