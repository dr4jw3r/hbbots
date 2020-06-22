from time import sleep
from cv2 import imread
#
from lib.inputcontrol import moveto, keydown, keyup, rightdown, rightup, click
from lib.inventory import openinventory, closeinventory, getbounds
from lib.imagesearch import imagesearch_fromscreenshot_withtemplate
# 
from farmbot.positions import Position, PLANTING_POSITIONS

class Planter(object):
    def __init__(self, screenshot_thread):
        self.screenshot_thread = screenshot_thread

        self.SEED_BAG_IMAGE = imread("./common/samples/inventory/seed_bag.png", 0)
        self.SEED_BAG_PRECISION = 0.7

    def plantsingle(self, position, cancellation_token):
        has_bag = self._clickbag(cancellation_token)
        if has_bag:
            moveto((position.x, position.y))
            sleep(0.3)

            if cancellation_token.is_cancelled:
                return False

            click()
            sleep(0.3)

        return has_bag

    def replant(self, values, cancellation_token):
        for i in range(len(values)):
            if cancellation_token.is_cancelled:
                break

            if values[i]:
                self.plantsingle(PLANTING_POSITIONS[i], cancellation_token)
    
    def findseedbag(self, cancellation_token):
        openinventory()
        RETRY_COUNT = 5
        BAG_OFFSET = 10
        bounds = getbounds()

        screenshot = self.screenshot_thread.croppedcoordinates(bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1])

        for i in range(RETRY_COUNT):
            if cancellation_token.is_cancelled:
                return (-1, -1)

            seed_bag_pos = imagesearch_fromscreenshot_withtemplate(self.SEED_BAG_IMAGE, screenshot, self.SEED_BAG_PRECISION)
            if seed_bag_pos[0] != -1:
                x = seed_bag_pos[0] + bounds[0][0] + BAG_OFFSET
                y = seed_bag_pos[1] + bounds[0][1] + BAG_OFFSET

                return (x, y)

        return (-1, -1)

    def _clickbag(self, cancellation_token):
        bag_pos = self.findseedbag(cancellation_token)

        if bag_pos[0] == -1:
            return False

        moveto(bag_pos)
        sleep(0.05)

        if cancellation_token.is_cancelled:
            return False

        click(2)
        sleep(0.1)
        return True    