from time import sleep
# 
from lib.inventory import openinventory, wandposition, hoepositions, weaponsposition
from lib.inputcontrol import moveto, keydown, keyup, click

def equipstaff():
    openinventory()
    sleep(0.05)
    moveto(wandposition())
    sleep(0.1)
    keydown("ctrlleft")
    click()
    keyup("ctrlleft")
    sleep(0.1)

def equiphoe(hoe_index, ocr):
    openinventory()
    sleep(0.05)

    try:
        hoe_pos = hoepositions()[hoe_index]
    except IndexError:
        return False

    if hoe_pos[0] != -1:
        moveto(hoe_pos)
        sleep(0.1)
        click(2, 0.05)
        sleep(0.2)

    sleep(0.2)
    is_exhausted = ocr.checkexhausted()
    sleep(0.2)
    return not is_exhausted

def equipweapon():
    openinventory()
    moveto(weaponsposition())
    sleep(0.1)
    keydown("ctrlleft")
    click()
    keyup("ctrlleft")
    sleep(0.1)

