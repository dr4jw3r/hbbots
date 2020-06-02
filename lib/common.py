import re
###########
from time import sleep, time
###########
from lib.ocr import OCR
from lib.LocationMonitor import LocationMonitor
from lib.imagesearch import imagesearch_numLoop, imagesearch, imagesearcharea
from lib.inputcontrol import keydown, keyup, keypress, moveto, click, clickright
from lib.inputcontrol import leftdown as mouseleftdown, leftup as mouseleftup, rightdown as mouserightdown, rightup as mouserightup
from lib.inventory import openinventory, closeinventory, defaultposition, inventorypositions, wandposition
from lib.charmove import *
###########
from lib.threads.castspell import CastSpellThread

# CONSTANTS #
OCR = OCR()
LocationMonitor = LocationMonitor()
SELF_POSITION = (400, 280)

# CHECKS #
def checkifdead():
    pos = imagesearch("./common/samples/misc/restart.png")
    if pos[0] is not -1:
        return True

    return False

def checkforenemies(cancellation_token):
    cursor_image = "./common/samples/misc/cursor.png"
    precision = 0.4427884615384618
    positions = [
        ( 367, 260 ),
        ( 397, 260 ),
        ( 430, 260 ),
        ( 433, 305 ),
        ( 433, 333 ),
        ( 396, 333 ),
        ( 367, 330 ),
        ( 367, 300 )
    ]

    for pos in positions:
        if cancellation_token.is_cancelled:
            break
            
        moveto(pos)
        sleep(0.05)
        pos = imagesearcharea(cursor_image, 335, 225, 480, 370, precision)
        if pos[0] != -1:
            return True
    
    return False
        

# ACTIONS #
def _movemeat(meat_type):
    moveto((10, 10))
    openinventory()

    pos = imagesearch_numLoop("./common/samples/inventory/" + meat_type + ".png", 0.1, 5, 0.7)

    if pos[0] != -1:
        moveto(pos, 10)
        sleep(0.1)
        keydown("shiftleft")
        mouseleftdown()
        sleep(0.1)
        moveto((585, 429))
        sleep(0.1)
        mouseleftup()
        sleep(0.1)
        keyup("shiftleft")
        sleep(0.1)

    closeinventory()

    return True if pos[0] != -1 else False

def _eatmeat(meat_type):
    moveto((10, 10))
    openinventory()
    pos = [0, 0]
    
    while pos[0] is not -1:
        pos = imagesearch_numLoop("./common/samples/inventory/" + meat_type + ".png", 0.1, 5)

        if pos[0] != -1:
            moveto(pos, 10)
            sleep(0.1)
            click(2, 0.05)
            moveto((10, 10))

    closeinventory()

def restart():
    pos = imagesearch("./common/samples/misc/restart.png")
    moveto(pos, 5)
    sleep(0.1)
    click()

def chugpots():
     for i in range(5):
        keypress("1")
        sleep(0.5)
        keypress("2")
        sleep(0.5)
        keypress("3")
        sleep(0.5)

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

def eatmeat(meat_type):
    has_meat = _movemeat(meat_type)

    if has_meat:
        sleep(0.5)
        _eatmeat(meat_type)
        sleep(0.5)

    return has_meat

def disenchant(cancellation_token):
    openinventory()
    keydown("ctrlleft")
    keypress("e")
    keyup("ctrlleft")

    if cancellation_token.is_cancelled:
        return

    sleep(0.1)
    pos = imagesearch_numLoop("./common/samples/buttons/disenchant_main.png", 0.1, 10)
    moveto(pos,25)
    sleep(0.2)
    click()
    sleep(0.1)

    if cancellation_token.is_cancelled:
        return

    for position in inventorypositions():
        if cancellation_token.is_cancelled:
            return

        moveto(position)
        sleep(0.01)
        click(2, 0.01)

    if cancellation_token.is_cancelled:
        return

    sleep(5)

    if cancellation_token.is_cancelled:
        return

    pos = imagesearch_numLoop("./common/samples/buttons/disenchant.png", 0.1, 10)
    moveto(pos, 15)
    click()
    keydown("ctrlleft")
    keypress("e")
    keyup("ctrlleft")
    sleep(0.5)
    closeinventory()

def repairgear(cancellation_token):
    has_repaired = False
    
    while not has_repaired:
        if cancellation_token.is_cancelled:
            return

        clicknpc("blacksmith", cancellation_token)        

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
    clicknpc("blacksmith", cancellation_token)
    
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

# EQUIPMENT #
def equipstaff():
    openinventory()
    moveto(wandposition())
    sleep(0.05)
    keydown("ctrlleft")
    click()
    keyup("ctrlleft")
    closeinventory()
    sleep(1)

# SPELLS #
def recall(cancellation_token):
    CastSpellThread("recall")
    sleep(2)
    moveto(SELF_POSITION)
    sleep(0.1)

    if cancellation_token.is_cancelled:
        return

    click()
    sleep(2)

def saferecall(cancellation_token):
    current_location = None
    while current_location is None:
        current_location = OCR.getlocation()

        if current_location is not None:
            current_location = current_location[0]
            new_location = current_location

    while current_location is new_location:
        if cancellation_token.is_cancelled:
            return

        recall(cancellation_token)
        sleep(0.1)
        location = OCR.getlocation()
        if location is not None:
            new_location = location[0]        

def createfood(cancellation_token):
    CastSpellThread("createfood")
    sleep(2)
    moveto(SELF_POSITION)
    sleep(0.1)

    if cancellation_token.is_cancelled:
        return

    click()
    sleep(2)

# MOVEMENT #
def followwpts(cancellation_token, wpts, locationstop=None, tolerance=2):
    for point in wpts:
        if point == wpts[-1]:
            delay = 1
        else:
            delay = 0

        onpoint = False

        direction = [-1, -1]
        while not onpoint:
            if cancellation_token.is_cancelled:
                break

            (onpoint, direction) = runto(direction, point, delay, locationstop, tolerance)

def runto(direction, coords, delay=0, locationstop=None, tolerance=2):
    sleep(delay)    

    current_loc = LocationMonitor.getlocation()
    current_coords = LocationMonitor.getcoordinates()

    if locationstop is not None and current_loc is not None:
        if current_loc.find(locationstop) != -1:
            mouserightdown()
            sleep(0.5)
            mouserightup()

            return (True, [0, 0])   

    if current_coords is not None:        
        direction[0] = int(current_coords[0]) - coords[0]
        direction[1] = int(current_coords[1]) - coords[1]
    else:
        direction[0] = 1
        direction[1] = 1

    if (direction[0] <= tolerance and direction[0] >= -tolerance) and (direction[1] <= tolerance and direction[1] >= -tolerance):
        mouserightdown()
        sleep(0.5)
        mouserightup()
        return (True, direction)
    elif direction[0] > 0 and direction[1] > 0:
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

    current_loc = LocationMonitor.getlocation()
    current_coords = LocationMonitor.getcoordinates()

    if locationstop is not None and current_loc is not None:
        if current_loc.find(locationstop) != -1:
            mouserightdown()
            sleep(0.5)
            mouserightup()

            return (True, [0, 0])        

    return (False, direction)

def gotoblacksmith_fromrecall(cancellation_token):
    has_blacksmith = False
    BS_WPTS = [
        [58, 101],
        [65, 96],
        [64, 91]
    ]

    while not has_blacksmith:
        followwpts(cancellation_token, BS_WPTS, "Blacksmith")
        sleep(1)

        if cancellation_token.is_cancelled:
            break

        (pos, has_blacksmith) = findnpc("blacksmith")

def gotoshop_fromrecall(cancellation_token):
    has_shopkeeper = False
    SHOP_WPTS = [
        (61, 72),
        (61, 50)
    ]

    while not has_shopkeeper:
        followwpts(cancellation_token, SHOP_WPTS, "Shop")
        sleep(1)

        if cancellation_token.is_cancelled:
            break

        (pos, has_shopkeeper) = findnpc("shopkeeper")

# NPC ACTIONS #
def clickbutton(button, cancellation_token, offsetX=0, offsetY=0):
    moveto((0, 0))
    button_pos = imagesearch_numLoop("./common/samples/buttons/" + button + ".png", 0.1, 5)
    moveto(button_pos, offsetX, offsetY)
    sleep(0.1)
    click()

def findnpc(npc):
    pos = imagesearch_numLoop("./common/samples/monsters/" + npc + ".png", 0.1, 5)
    return (pos, pos[0] != -1)

def clicknpc(npc, cancellation_token):
    has_npc = False
    npc_pos = [-1, -1]
    while not has_npc:
        if cancellation_token.is_cancelled:
            return

        (npc_pos, has_npc) = findnpc(npc)

    moveto(npc_pos, 30)
    sleep(0.1)
    click()  