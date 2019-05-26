from ctypes import *
from time import sleep
from imagesearch import *

import pyautogui

user32 = windll.user32

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.05

# Presses and releases mouse
def click(times=1):
        for i in range(0, times):
            user32.mouse_event(0x0002, 0, 0, 0, 0)
            sleep(0.1)
            user32.mouse_event(0x0004, 0, 0, 0, 0)
            sleep(0.1)

def rightdown():
    user32.mouse_event(0x0008, 0, 0, 0, 0)

def rightup():
    user32.mouse_event(0x0010, 0, 0, 0, 0)

def moveto(pos):
    if pos[0] != -1:
        pyautogui.moveTo(pos[0], pos[1])

def findcursor():
    pos = imagesearch("./samples/cursor.png", 0.45)
    return pos[0] != -1

def checkfordrops():
    DROPS = [
        "bodice",
        "cap",
        "falchion",
        "falchion2",
        "falchion3",
        "gladius",
        "mallet",
        "ring",
        "saxonaxe",
        "scutum",
        "shirtM",
        "targeshield",
        "tomahawk",
        "trousersM",
        "tunic",
        "wand",
        "wand2",
        "wand3",
        "woodshield"
    ]

    for i in range(0, len(DROPS)):
        pos = imagesearch("./samples/" + DROPS[i] + ".png", 0.7)

        if pos[0] != -1:
            moveto([ pos[0] + 5, pos[1] + 5 ])
            click()
            sleep(2)
            moveto([400, 300])
            click()

def findorc(idx):
    pos = imagesearch("./samples/gold.png", 0.6)

    if pos[0] != -1:
        moveto(pos)
        click()
        sleep(1)

    checkfordrops()

    pos = imagesearch("./samples/" + str(idx) + ".png", 0.4)    

    if pos[0] != -1:
        pos = [ pos[0] + 25, pos[1] + 25 ]
        moveto(pos)

        rightdown()

        while findcursor():
            sleep(0.1)

        rightup()

    idx += 1
    if idx >= 8:
        idx = 1

    sleep(0.1)
    findorc(idx)

def runloop():
    findorc(1)

#####################################################

sleep(5)
runloop()
