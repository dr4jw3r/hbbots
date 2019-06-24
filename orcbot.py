from ctypes import *
from time import sleep
from imagesearch import *
from gold import checkforgold
from drops import checkfordrops
from threading import Thread
from inputcontrol import *

import pyautogui

class OrcThread(object):
    def __init__(self):
        self.idx = 1
        self.keeprunning = True
        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        print("going")
        while self.keeprunning:
            self.findorc()

    def stop(self):
        self.keeprunning = False

    def findcursor(self):
        pos = imagesearch("./common/samples/misc/cursor.png", 0.45)
        return pos[0] != -1

    def findorc(self):
        checkforgold()
        checkfordrops()

        pos = imagesearch("./common/samples/monsters/orc_" + str(self.idx) + ".png", 0.4)    

        if pos[0] != -1:
            pos = [ pos[0] + 25, pos[1] + 25 ]
            moveto(pos)

            rightdown()

            while self.findcursor():
                sleep(0.1)

            rightup()

        self.idx += 1
        if self.idx >= 8:
            self.idx = 1