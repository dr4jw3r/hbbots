import pyautogui, time
from imagesearch import *

time.sleep(5)
pyautogui.click()    # click to put drawing program in focus
distance = 0

def testcursor():
    pos = imagesearch("./common/samples/misc/cursor_magic_red.png")

    print(pos)

    if pos[0] != -1: 
        print("found!")

offset = 33.3

pyautogui.moveTo(400, 300)

hor = 0
ver = 0

for i in range(0, 6):
    hor = hor + 1
    ver = ver + 1

    for h in range(0, hor):
        pyautogui.moveRel(offset, 0)
        time.sleep(.5)
        testcursor()

    for v in range(0, ver):
        pyautogui.moveRel(0, offset)
        time.sleep(.5)
        testcursor()

    hor = hor + 1
    ver = ver + 1

    for h in range(0, hor):
        pyautogui.moveRel(-offset, 0)
        time.sleep(.5)
        testcursor()

    for v in range(0, ver):
        pyautogui.moveRel(0, -offset)
        time.sleep(.5)
        testcursor()
