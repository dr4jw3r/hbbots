from imagesearch import *
from inputcontrol import *

SCREENWIDTH = 800
SCREENHEIGHT = 600
SCREENSIZE = (0, 0, SCREENWIDTH, SCREENHEIGHT)
SCREENCENTER = [400, 300]
CLICKOFFSET = 5

p1 = (319, 222)
p2 = (481, 383)

DROPS = [
    ("bodice", 0.7, True),
    ("cap", 0.7, True),
    ("falchion", 0.7, True),
    ("falchion2", 0.7, True),
    ("falchion3", 0.7, True),
    ("gladius", 0.7, True),
    ("mallet", 0.7, True),
    ("merien", 0.8, True),
    ("ring", 0.72, True),
    ("saxonaxe", 0.7, True),
    ("scutum", 0.7, True),
    ("shirtM", 0.7, True),
    ("targeshield", 0.7, True),
    ("tomahawk", 0.7, True),
    ("trousersM", 0.7, True),
    ("trousersW", 0.8, True),
    ("tunic", 0.7, True),
    ("wand", 0.7, True),
    ("wand2", 0.7, True),
    ("wand3", 0.7, True),
    ("woodshield", 0.7, True),
    ("xelima", 0.75, True),
    ("zem", 0.85, True),
    ("zem2", 0.8, True),
    # ==================
    # BODY PARTS
    # ==================
    ("slimejelly", 0.7, True),
    ("snakeskin", 0.55, True),
    ("snakemeat", 0.8, False),
    ("snaketeeth", 0.85, True),
    ("snaketongue", 0.55, True),
    ("antlegs", 0.8, True),
    ("antantenna", 0.7, True),
    ("lg_antantenna", 0.6, True),
    ("lg_antlegs", 0.8, True)
]

def checkfordrops(runtime=1):
    im = region_grabber(SCREENSIZE)

    for i in range(0, len(DROPS)):
        if DROPS[i][2] == False:
            continue

        pos = imagesearcharea("./common/samples/drops/" + DROPS[i][0] + ".png", 0, 0, SCREENWIDTH, SCREENHEIGHT, DROPS[i][1], im)

        if pos[0] != -1:
            print(DROPS[i])
            moveto([ val + CLICKOFFSET for val in pos ])
            sleep(0.05)
            click()
            sleep(runtime)
            moveto(SCREENCENTER)
            click()