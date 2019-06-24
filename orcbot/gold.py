from time import sleep
from imagesearch import imagesearcharea
from inputcontrol import moveto, click

p1 = (350, 255)
p2 = (450, 350)

def checkforgold():
    pos = imagesearcharea("./common/samples/drops/gold.png", p1[0], p1[1], p2[0], p2[1], 0.65)
    if pos[0] != -1:
        newpos = (pos[0] + p1[0], pos[1] + p1[1])
        moveto(newpos)
        click()