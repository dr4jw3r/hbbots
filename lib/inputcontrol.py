import pyautogui

from time import sleep
from ctypes import *

user32 = windll.user32

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

def moveto(pos, offsetX=0, offsetY=None, duration=0):
    if pos[0] != -1:
        if offsetY is None:
            offsetY = offsetX

        pos = (pos[0] + offsetX, pos[1] + offsetY)
        pyautogui.moveTo(pos[0], pos[1], duration=duration)

def click(times=1, sleeptime=0, duration=0.05):
    for i in range(0, times):
        user32.mouse_event(0x0002, 0, 0, 0, 0)
        sleep(duration)
        user32.mouse_event(0x0004, 0, 0, 0, 0)
        sleep(sleeptime)

def clickright(times=1, sleeptime=0, duration=0.05):
    for i in range(0, times):
        user32.mouse_event(0x0008, 0, 0, 0, 0)
        sleep(duration)
        user32.mouse_event(0x0010, 0, 0, 0, 0)
        sleep(sleeptime)


def leftdown():
    user32.mouse_event(0x0002, 0, 0, 0, 0)        

def leftup():
    user32.mouse_event(0x0004, 0, 0, 0, 0)

def rightdown():
    user32.mouse_event(0x0008, 0, 0, 0, 0)

def rightup():
    user32.mouse_event(0x0010, 0, 0, 0, 0)

def keypress(key):
    pyautogui.press(key)

def keydown(key):
    pyautogui.keyDown(key)

def keyup(key):
    pyautogui.keyUp(key)

def inputdisable():
    windll.user32.BlockInput(True)

def inputenable():
    windll.user32.BlockInput(False)

def position():
    return pyautogui.position()
    