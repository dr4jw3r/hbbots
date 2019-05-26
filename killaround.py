import random
#====
from threading import Thread
from time import sleep
from imagesearch import *
#====
from inputcontrol import *
from drops import checkfordrops
from gold import checkforgold
#====

class KillAroundThread(object):
    def __init__(self):
        self.POSITIONS = [
            ( 367, 272 ),
            ( 397, 267 ),
            ( 430, 272 ),
            ( 433, 305 ),
            ( 433, 333 ),
            ( 396, 333 ),
            ( 367, 330 ),
            ( 367, 300 )
        ]
        self.OUTER = [
            ( 336, 238 ),
            ( 367, 238 ),
            ( 398, 238 ),
            ( 429, 238 ),
            ( 460, 238 ),
            ( 460, 271 ),
            ( 460, 304 ),
            ( 460, 337 ),
            ( 460, 370 ),
            ( 429, 370 ),
            ( 398, 370 ),
            ( 367, 370 ),
            ( 336, 370 ),
            ( 336, 337 ),
            ( 336, 304 ),
            ( 336, 271 )
        ]

        self.keeprunning = True
        self.dropindex = 0
        
        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def finddrops(self):
        self.dropindex += 1
        if self.dropindex % 10 == 1:
            self.dropindex = 1
            checkfordrops()

    def run(self):
        scanouter = False
        index = 0
        critcounter = 0
        scancount = 0
        clickleftcount = 0

        while self.keeprunning:                   
            if scancount >= 2:
                scanouter = True

            if not scanouter:
                moveto(self.POSITIONS[index])
            else:
                moveto(self.OUTER[index])
                
            sleep(0.05)
            pos = imagesearch("./common/samples/misc/cursor.png", 0.45)

            if pos[0] == -1:
                checkforgold()
                self.finddrops()
                critcounter = 0
                keyup("altleft")
                rightup()
                index += 1

                if not scanouter:
                    if index > len(self.POSITIONS) - 1:
                        index = 0
                        scancount += 1
                else:
                    if index > len(self.OUTER) - 1:
                        index = 0
                        scancount = 0
                        scanouter = False
            else:
                if scanouter:
                    keydown("ctrlleft")
                    click()
                    keyup("ctrlleft")
                    index = 0
                else:
                    clickleftcount += 1

                    if clickleftcount >= 10:
                        click()
                        clickleftcount = 0

                    rightdown()
                    critcounter += 1
                    
                scancount = 0
                scanouter = False

            if critcounter >= 50:
                keydown("altleft")
                if critcounter >= 60:
                    critcounter = 0
                    keyup("altleft")

        # Stopped
        keyup("altleft")
        rightup()

    def stop(self):
        self.keeprunning = False