from imagesearch import *
from inputcontrol import *
from time import sleep

duration = 0.101
pos = (1, 1)

for i in range(0, 15):
    pos = imagesearch("./common/samples/misc/supercoal.png")
    moveto(pos, 5)
    sleep(0.05)
    leftdown()
    sleep(0.05)
    moveto((400, 300), duration=duration)
    leftup()
    sleep(0.05)