from time import sleep

from lib.imagesearch import imagesearch_numLoop, imagesearch
from lib.inputcontrol import keydown, keyup, keypress, moveto, click, leftdown as mouseleftdown, leftup as mouseleftup
from lib.inventory import openinventory, closeinventory, inventorypositions

# CHECKS #
def checkifdead():
    pos = imagesearch("./common/samples/misc/restart.png")
    if pos[0] is not -1:
        return True

    return False

# ACTIONS #
def restart():
    pos = imagesearch("./common/samples/misc/restart.png")
    moveto(pos, 5)
    sleep(0.1)
    click()

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

def chugpots():
     for i in range(5):
        keypress("1")
        sleep(0.5)
        keypress("2")
        sleep(0.5)
        keypress("3")
        sleep(0.5)

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