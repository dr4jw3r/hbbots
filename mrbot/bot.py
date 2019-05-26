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
        print("Position: ", pos[0], pos[1])
        pyautogui.moveTo(pos[0], pos[1])
    else:
        print("item not found")

def eat():
    pyautogui.press("f2")
    sleep(2)

    click(2)

    pyautogui.press("f6")
    sleep(1)
    pos = imagesearch("./samples/meat.png")
    moveto(pos)
    click(2)

    pos = imagesearch("./samples/baguette.png")
    sleep(1)
    moveto(pos)
    click(2)

    pyautogui.press("f6")

def missile():
    pyautogui.moveTo(400, 300)
    pyautogui.press("f3")
    sleep(2)
    click()

def equipshield():
    pyautogui.press("f6")
    pos = imagesearch("./samples/shield.png")
    moveto(pos)
    click(2)
    pyautogui.press("f6")

def runloop():
    while True:
        pyautogui.moveTo(400, 300)
        eat()

        for i in range(0, 95):
            missile()

        equipshield()

        sleep(600)

#####################################################
sleep(5)
runloop()
