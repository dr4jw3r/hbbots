from inputcontrol import *
from imagesearch import imagesearch_loop

POSITIONS = [
    ( 367, 200 ),
    ( 397, 200 ),
    ( 430, 200 ),
    ( 433, 305 ),
    ( 433, 333 ),
    ( 396, 333 ),
    ( 367, 330 ),
    ( 367, 300 )
]

posindex = 0

while True:
    pos = imagesearch_loop("./common/samples/misc/pretendcorpse.png", 0.1)
    moveto(pos, 5)
    for i in range(1):
        click()

    if posindex == len(POSITIONS) - 1:
        posindex = 0
    else:
        posindex += 1

    moveto(POSITIONS[posindex])
    sleep(0.05)
    clickright(duration=0.01)
