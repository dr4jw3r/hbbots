from imagesearch import *
from inputcontrol import *

SCREENWIDTH = 800
SCREENHEIGHT = 600
SCREENSIZE = (0, 0, SCREENWIDTH, SCREENHEIGHT)
SCREENCENTER = [400, 300]
CLICKOFFSET = 5
DROPS = [
    ("bodice", 0.7),
    ("cap", 0.7),
    ("falchion", 0.7),
    ("falchion2", 0.7),
    ("falchion3", 0.7),
    ("gladius", 0.7),
    ("mallet", 0.7),
    ("merien", 0.75),
    ("ring", 0.72),
    ("saxonaxe", 0.7),
    ("scutum", 0.7),
    ("shirtM", 0.7),
    ("targeshield", 0.7),
    ("tomahawk", 0.7),
    ("trousersM", 0.7),
    ("trousersW", 0.7),
    ("tunic", 0.7),
    ("wand", 0.7),
    ("wand2", 0.7),
    ("wand3", 0.7),
    ("woodshield", 0.7),
    ("xelima", 0.75),
    ("zem", 0.8),
    ("zem2", 0.8)
]

def checkfordrops(runtime=1):
    im = region_grabber(SCREENSIZE)

    for i in range(0, len(DROPS)):
        pos = imagesearcharea("./common/samples/drops/" + DROPS[i][0] + ".png", 0, 0, SCREENWIDTH, SCREENHEIGHT, DROPS[i][1], im)

        if pos[0] != -1:
            print(DROPS[i])
            moveto([ val + CLICKOFFSET for val in pos ])
            click()
            sleep(runtime)
            moveto(SCREENCENTER)
            click()