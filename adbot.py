from threading import Thread
from inputcontrol import keypress
from time import sleep

class AdThread(object):
    def __init__(self):
        self.text = "!trade sot|cic3hp50 rh M + 3|hp41 light plate M|hp39light fh M"

        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        sleep(0.5)

        for letter in self.text:
            keypress(letter)