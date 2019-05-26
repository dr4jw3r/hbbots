import pyautogui
from time import sleep
from imagesearch import *
from ctypes import *

user32 = windll.user32

class item:
    def __init__(self, name):
        self.name = name

class items:
    supercoal = item("super_coal")
    ironingot = item("iron_ingot")
    gladius = item("gladius")

# Presses and releases mouse
def click(times=1):
        for i in range(0, times):
            user32.mouse_event(0x0002, 0, 0, 0, 0)
            sleep(0.1)
            user32.mouse_event(0x0004, 0, 0, 0, 0)
            sleep(0.1)

def moveto(pos):
    if pos[0] != -1:
        print("Position: ", pos[0], pos[1])
        pyautogui.moveTo(pos[0], pos[1])
    else:
        print("item not found")
        exit(0)

def sellitems():
    blacksmith()

def blacksmith(amt=1):
    pos = imagesearch_loop("./samples/blacksmith.png", 0.2)
    pos = [pos[0] + 10, pos[1] + 10]
    moveto(pos)
    click()

    pos = imagesearch_loop("./samples/blacksmith_sell.png", 0.2)
    pos = [pos[0] + 10, pos[1] + 10]
    moveto(pos)
    click()

    for i in range(0, amt):
        pos = imagesearch_loop("./samples/bag_gladius.png", 0.2)
        pos = [pos[0] + 15, pos[1] + 10]
        moveto(pos)
        click(2)

    pos = imagesearch_loop("./samples/blacksmith_sell_button.png", 0.2)
    moveto(pos)
    click()

def finditem(item):
    pos = imagesearch_loop("./samples/" + item.name + ".png", 0.2)
    moveto(pos)
    click()

def make(amount=1):
    for i in range(0, amount):
        pos = imagesearch_loop("./samples/manufacture.png", 0.2)
        moveto(pos)
        click()
        pos = imagesearch_loop("./samples/back.png", 0.2)
        moveto(pos)
        click()

    click()

def makegladius():
    finditem(items.supercoal)
    make(2)
    finditem(items.ironingot)
    make()
    finditem(items.gladius)
    make()

#####################################################

count = 0
sell = False

for i in range(0, 34):
    makegladius()
    count = count + 1

    if sell and count == 10:
        blacksmith(10)
        count = 0

if sell and count != 0:
    blacksmith(count)