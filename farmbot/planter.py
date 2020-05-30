from time import sleep
#
from lib.inputcontrol import moveto, keydown, keyup, rightdown, rightup, click
from lib.inventory import openinventory, closeinventory, getbounds
from lib.imagesearch import imagesearcharea, region_grabber
# 
from farmbot.positions import Position, PLANTING_POSITIONS

class Planter(object):
    def __init__(self):
        self.SEED_BAG_IMAGE = "./common/samples/inventory/seed_bag.png"
        self.SEED_BAG_PRECISION = 0.7

    def plantall(self):
        openinventory()
        self._clickbag()
        closeinventory()

    def _clickbag(self):
        bag_pos = self._findseedbag()
        moveto(bag_pos)
        sleep(0.05)
        click(2)

    def _findseedbag(self):
        RETRY_COUNT = 5
        BAG_OFFSET = 10
        bounds = getbounds()

        img = region_grabber((bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1]))

        for i in range(RETRY_COUNT):
            seed_bag_pos = imagesearcharea(self.SEED_BAG_IMAGE, -1, -1, -1, -1, precision=self.SEED_BAG_PRECISION, im=img)
            if seed_bag_pos[0] != -1:
                x = seed_bag_pos[0] + bounds[0][0] + BAG_OFFSET
                y = seed_bag_pos[1] + bounds[0][1] + BAG_OFFSET

                return (x, y)

        return (-1, -1)

    