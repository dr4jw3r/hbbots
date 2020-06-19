from ctypes import *
from time import sleep

from threading import Thread

from lib.threads.killaround import KillAroundThread

from lib.imagesearch import *
from lib.pickup_gold import checkforgold
from lib.pickup_drops import checkfordrops
from lib.inputcontrol import *
from lib.utils.CancellationToken import CancellationToken
from lib.utils.ScreenshotThread import ScreenshotThread
from lib.ocr import OCR

import pyautogui

class OrcThread(object):
    def __init__(self):
        self.scanindex = 0
        self.idx = 1
        self.keeprunning = True
        self.killaroundthread = None

        self.cancellation_token = CancellationToken()
        self.ocr = OCR(ScreenshotThread(self.cancellation_token))
        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while self.keeprunning:
            self.findorc()

    def stop(self):
        self.keeprunning = False
        if self.killaroundthread is not None:
            self.killaroundthread.stop()

    def findcursor(self):
        pos = imagesearch("./common/samples/misc/cursor.png", 0.45)
        return pos[0] != -1

    def checkaround(self):
        self.killaroundthread = KillAroundThread(self.ocr, singlescan=True)
        self.killaroundthread = None

    def findorc(self):
        checkforgold()
        # checkfordrops()

        self.scanindex += 1
        if self.scanindex % 10 == 0:
            self.checkaround()
            self.scanindex = 0

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