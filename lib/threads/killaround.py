import random
#====
from threading import Thread
from time import sleep, time
#====
from lib.imagesearch import *
from lib.inputcontrol import *
from lib.pickup_gold import checkforgold
from lib.pickup_drops import checkfordrops
from lib.common import chugpots, disenchant, eatmeat, checkifdead
from lib.ocr import OCR
from lib.CancellationToken import CancellationToken
#====

class KillAroundThread(object):
    def __init__(self, meat_type=None, singlescan=False, no_loot=False):
        self.meat_type = meat_type
        self.no_loot = no_loot
        self.singlescan = singlescan
        self.OCR = OCR()
        self.cancellation_token = CancellationToken()
        self.POSITIONS = [
            ( 367, 260 ),
            ( 397, 260 ),
            ( 430, 260 ),
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
        
        self.thread = Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def checkinventory(self):
        if self.OCR.inventoryfull():
            rightup()
            chugpots()
            sleep(0.5)

            if self.meat_type is not None:
                eatmeat(self.meat_type)
                sleep(0.5)
            
            disenchant(self.cancellation_token)
            sleep(0.5)

            if self.meat_type is not None:
                eatmeat(self.meat_type)

    def finddrops(self):
        self.dropindex += 1
        if self.dropindex % 10 == 1:
            self.dropindex = 1
            return checkfordrops()

        return False

    def run(self):
        CRITCOUNTER = 30
        reverse = False
        scanouter = False
        index = 0
        critcounter = 0
        scancount = 0
        clickleftcount = 0
        indexes = random.sample(range(0, 8), 8)

        while self.keeprunning:                           
            if scancount >= 3:
                scanouter = True

            if not scanouter:
                moveto(self.POSITIONS[indexes[index]])
            else:
                moveto(self.OUTER[index])
                
            sleep(0.08)

            if not scanouter and indexes[index] >= 0 and indexes[index] <= 2:
                # precision = 0.45
                precision = 0.4427884615384618
            else:
                # precision = 0.45
                precision = 0.4427884615384618
            
            pos = imagesearch("./common/samples/misc/cursor.png", precision)

            # If sword cursor has NOT been found
            if pos[0] == -1:
                if not self.no_loot:
                    checkforgold()
                    has_drop = self.finddrops()

                    if has_drop:
                        sleep(0.2)
                        self.checkinventory()

                critcounter = 0
                keyup("altleft")
                rightup()
                index += 1

                # Keep scanning inner circle
                if not scanouter:
                    if index >= len(self.POSITIONS):

                        if self.singlescan:
                            self.stop()

                        index = 0
                        indexes = random.sample(range(0, 8), 8)
                        scancount += 1
                # Scan outer circle
                else:
                    if index >= len(self.OUTER):
                        index = 0
                        scancount = 0
                        scanouter = False
            
            # If sword cursor has been found
            else:
                elitepos = imagesearch("./common/samples/misc/elite.png", 0.8)
                iselite = elitepos[0] != -1

                if scanouter:
                    keydown("ctrlleft")
                    click()
                    keyup("ctrlleft")
                    index = 0
                    indexes = random.sample(range(0, 8), 8)
                else:
                    if iselite:
                        keydown("altleft")
                        
                    clickleftcount += 1

                    if clickleftcount >= 10:
                        click()
                        clickleftcount = 0

                    rightdown()
                    critcounter += 1
                    
                scancount = 0
                scanouter = False

            if checkifdead():
                self.stop()
                break

            if critcounter >= CRITCOUNTER:
                keydown("altleft")
                if critcounter >= CRITCOUNTER * 2.5:
                    critcounter = 0
                    keyup("altleft")

        # Stopped
        keyup("altleft")
        rightup()

    def stop(self):
        keyup("altleft")
        keyup("ctrlleft")
        rightup()

        self.keeprunning = False

    def join(self):
        self.thread.join()