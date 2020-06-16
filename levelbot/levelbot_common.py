import re

from time import sleep, time

from lib.inputcontrol import keypress, keydown, keyup, moveto, click, clickright, leftdown as mouseleftdown, leftup as mouseleftup
from lib.imagesearch import imagesearch, imagesearch_numLoop
from lib.ocr import OCR
from lib.charmove import *
from lib.inventory import openinventory, closeinventory, defaultposition, weaponsposition, wandposition, inventorypositions
from lib.common import checkifdead, restart

from lib.threads.CastSpellThread import CastSpellThread
from lib.threads.killaround import KillAroundThread

OCR = OCR(None)

DISENCHANT_TIME = 5

### ACTIONS ###

def kill(cancellation_token, time):
    start = currentmillis()
    killthread = KillAroundThread()
            
    current_time = 0
    
    while current_time - start <= (time * 60000):
        if cancellation_token.is_cancelled:
            killthread.stop()
            killthread = None
            return

        if checkifdead():
            break

        current_time = currentmillis()   

        sleep(1)
            
    killthread.stop()
    killthread = None

### EQUIP ###

def equipweapon():
    openinventory()
    moveto(weaponsposition())
    sleep(0.1)
    keydown("ctrlleft")
    click()
    keyup("ctrlleft")
    sleep(0.1)
    closeinventory()

### MISC ###
def currentmillis():
    return int(round(time() * 1000))