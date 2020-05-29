from lib.imagesearch import *
from lib.inputcontrol import *
from lib.drops import DROPS

SCREENWIDTH = 800
SCREENHEIGHT = 600
SCREENSIZE = (0, 0, SCREENWIDTH, SCREENHEIGHT)
SCREENCENTER = [400, 300]
CLICKOFFSET = 5

GRABREGION = (319, 222, 481, 383)

def checkfordrops(runtime=1):
    im = region_grabber(GRABREGION)

    for i in range(0, len(DROPS)):
        if DROPS[i][2] == False:
            continue

        pos = imagesearcharea("./common/samples/drops/" + DROPS[i][0] + ".png", GRABREGION[0], GRABREGION[1], GRABREGION[2], GRABREGION[3], DROPS[i][1], im)

        if pos[0] != -1:
            print(DROPS[i][0])
            newpos = ((GRABREGION[0] + CLICKOFFSET + pos[0]), (GRABREGION[1] + CLICKOFFSET + pos[1]))
            moveto(newpos)
            sleep(0.05)
            click()
            sleep(runtime)
            moveto(SCREENCENTER)
            click()
            return True

    return False