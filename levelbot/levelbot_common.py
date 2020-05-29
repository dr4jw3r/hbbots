import re

from time import sleep, time

from lib.inputcontrol import keypress, keydown, keyup, moveto, click, clickright, leftdown as mouseleftdown, leftup as mouseleftup
from lib.imagesearch import imagesearch, imagesearch_numLoop
from lib.ocr import OCR
from lib.charmove import *
from lib.inventory import openinventory, closeinventory, defaultposition, weaponsposition, wandposition, inventorypositions
from lib.common import checkifdead, restart

from lib.threads.castspell import CastSpellThread
from lib.threads.killaround import KillAroundThread

OCR = OCR()

SELF_POSITION = (400, 280)
DISENCHANT_TIME = 5

### ACTIONS ###

def repairgear(cancellation_token):
    has_repaired = False
    
    while not has_repaired:
        if cancellation_token.is_cancelled:
            return

        clickblacksmith(cancellation_token)        

        repair_all_pos = [-1, -1]
        while repair_all_pos[0] == -1:
            if cancellation_token.is_cancelled:
                return
            
            repair_all_pos = imagesearch("./common/samples/buttons/repair_all.png")

            if repair_all_pos[0] != -1:
                moveto(repair_all_pos, 10)
                sleep(0.1)
                click()

        repair_pos = imagesearch_numLoop("./common/samples/buttons/repair.png", 0.1, 5)

        # Maybe nothing to repair
        if repair_pos[0] != -1:
            moveto(repair_pos, 10)
            sleep(0.1)
            click()

        has_repaired = True

def sellitems(cancellation_token):
    clickblacksmith(cancellation_token)
    
    sell_items_pos = [-1, -1]
    while sell_items_pos[0] == -1:
        if cancellation_token.is_cancelled:
            return

        sell_items_pos = imagesearch("./common/samples/buttons/sell_items.png")
        if sell_items_pos[0] != -1:
            moveto(sell_items_pos, 10)
            sleep(0.1)
            click()

            for position in inventorypositions():
                moveto(position)
                sleep(0.01)
                click(2, 0.01)

            # If any items to be sold - click button
            sell_button_pos = imagesearch_numLoop("./common/samples/buttons/sell_items_btn.png", 0.1, 10)
            moveto(sell_button_pos, 10)
            sleep(0.1)
            click()
            sleep(1)

            # If no items to be sold, close the list
            sell_list_pos = imagesearch_numLoop("./common/samples/misc/sell_list.png", 0.1, 5)
            if sell_list_pos[0] != -1:
                moveto(sell_list_pos)
                sleep(0.5)
                clickright()
                sleep(0.5)

            closeinventory()

def eat(cancellation_token, number):
    for i in range(0, number):
        if cancellation_token.is_cancelled:
            return

        createfood(cancellation_token)
        
    clickright()
    sleep(1)
    openinventory()
    moveto(defaultposition())
    sleep(0.1)
    click(number * 2, 0.05)
    sleep(0.05)
    closeinventory()

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

def equipstaff():
    openinventory()
    moveto(wandposition())
    sleep(0.05)
    keydown("ctrlleft")
    click()
    keyup("ctrlleft")
    closeinventory()
    sleep(1)

def equipweapon():
    openinventory()
    moveto(weaponsposition())
    sleep(0.1)
    keydown("ctrlleft")
    click()
    keyup("ctrlleft")
    sleep(0.1)
    closeinventory()

### FIND CHARACTERS ###

def findblacksmith():
    pos = imagesearch_numLoop("./common/samples/monsters/blacksmith.png", 0.1, 5)
    return (pos, pos[0] != -1)

def clickblacksmith(cancellation_token):
    has_blacksmith = False
    blacksmith_pos = [-1, -1]
    while not has_blacksmith:
        if cancellation_token.is_cancelled:
            return

        (blacksmith_pos, has_blacksmith) = findblacksmith()

    moveto(blacksmith_pos, 30)
    sleep(0.1)
    click()    


### CAST SPELLS ###

def recall(cancellation_token):
    CastSpellThread("recall")
    sleep(2)
    moveto(SELF_POSITION)
    sleep(0.1)

    if cancellation_token.is_cancelled:
        return

    click()
    sleep(2)

def createfood(cancellation_token):
    CastSpellThread("createfood")
    sleep(2)
    moveto(SELF_POSITION)
    sleep(0.1)

    if cancellation_token.is_cancelled:
        return

    click()
    sleep(2)



### MOVEMENT ###

def followwpts(cancellation_token, wpts, locationstop=None):
    for point in wpts:

        if point == wpts[-1]:
            delay = 0.5
        else:
            delay = 0.02

        onpoint = False

        direction = [-1, -1]
        while not onpoint:
            if cancellation_token.is_cancelled:
                break

            (onpoint, direction) = runto(direction, point, delay, locationstop)

def runto(direction, coords, delay=0.02, locationstop=None):
        sleep(delay)
        current_loc = OCR.getlocation()

        if locationstop is not None and current_loc is not None:
            if current_loc[0].find(locationstop) != -1:
                clickright()
                return (True, [0, 0])

        if current_loc is not None:
            current = current_loc[1]
            currentX = re.sub('[^0-9]', '', str(current[0]))
            currentY = re.sub('[^0-9]', '', str(current[1]))
            direction[0] = int(currentX) - coords[0]
            direction[1] = int(currentY) - coords[1]
        else:
            current_loc = ["None", direction]

        if direction[0] > 0 and direction[1] > 0:
            leftup(direction)
        elif direction[0] == 0 and direction[1] > 0:
            up(direction)
        elif direction[0] < 0 and direction[1] > 0:
            rightup(direction)
        elif direction[0] < 0 and direction[1] == 0:
            right(direction)
        elif direction[0] < 0 and direction[1] < 0:
            rightdown(direction)
        elif direction[0] == 0 and direction[1] < 0:
            down(direction)
        elif direction[0] > 0 and direction[1] < 0:
            leftdown(direction)
        elif direction[0] > 0 and direction[1] == 0:
            left(direction)
        elif direction[0] == 0 and direction[1] == 0:
            return (True, direction)

        return (False, direction)

def gotoblacksmith_fromrecall(cancellation_token):
    has_blacksmith = False
    BS_WPTS = [
        [63, 96],
        [63, 80]
    ]

    while not has_blacksmith:
        followwpts(cancellation_token, BS_WPTS, "Blacksmith")
        
        sleep(1)

        if cancellation_token.is_cancelled:
            break

        (pos, has_blacksmith) = findblacksmith()



### MISC ###
def currentmillis():
    return int(round(time() * 1000))