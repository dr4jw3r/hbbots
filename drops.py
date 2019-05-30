from imagesearch import *
from inputcontrol import *

SCREENWIDTH = 800
SCREENHEIGHT = 600
SCREENSIZE = (0, 0, SCREENWIDTH, SCREENHEIGHT)
SCREENCENTER = [400, 300]
CLICKOFFSET = 5

GRABREGION = (319, 222, 481, 383)

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
    im = region_grabber(GRABREGION)
    im.save("test.png")

    for i in range(0, len(DROPS)):
        if DROPS[i][2] == False:
            continue

        pos = imagesearcharea("./common/samples/drops/" + DROPS[i][0] + ".png", GRABREGION[0], GRABREGION[1], GRABREGION[2], GRABREGION[3], DROPS[i][1], im)

        if pos[0] != -1:
            print(DROPS[i])
            newpos = ((GRABREGION[0] + CLICKOFFSET + pos[0]), (GRABREGION[1] + CLICKOFFSET + pos[1]))
            print(pos, newpos)
            moveto(newpos)
            sleep(0.05)
            click()
            sleep(runtime)
            moveto(SCREENCENTER)
            click()