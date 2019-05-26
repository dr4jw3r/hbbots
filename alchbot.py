from inputcontrol import *
from imagesearch import *
from time import sleep

from pyautogui import position

# ======================
def clickitem(item, precision=0.5):
    pos = imagesearch_loop("./common/samples/alch/" + item + ".png", 0.5, precision=precision)

    # print(pos)

    if pos[0] != -1:
        moveto([x + 10 for x in pos])
        sleep(0.05)
        click(2, 0.26)

# ======================

def makehealthpotion():
    clickitem("alchemybowl", 0.9)
    sleep(0.5)
    clickitem("slimejelly", 0.8)
    sleep(0.5)
    clickitem("snaketongue")
    sleep(0.5)
    clickitem("antleg", 0.8)
    sleep(0.5)
    clickitem("trynow2", 0.5)

x = 550
y = 380
offset = 50

pos1 = (x, y)
pos2 = (x + offset, y)
pos3 = (x + offset * 2, y)
pos4 = (x + offset * 3, y)

sleep(10)
moveto(pos4)
click(2)
moveto(pos1)
click(2)
moveto(pos2)
click(2)
moveto(pos3)
click(2)
clickitem("trynow2", 0.5)
sleep(3)