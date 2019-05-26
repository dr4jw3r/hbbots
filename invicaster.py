from inputcontrol import keypress, moveto, click
from time import sleep

sleep(5)

while True:
    keypress("f2")
    moveto((400, 300))
    sleep(2)
    click()
    sleep(50)