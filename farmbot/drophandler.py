from time import sleep
from lib.inputcontrol import moveto, click, clickright
from lib.imagesearch import imagesearcharea
from farmbot.positions import SELF_POSITION

class DropHandler(object):
    def __init__(self):
        self.GRABREGION = (319, 222, 481, 383)

    def _getdrop(self, pos):
        moveto(pos)
        sleep(0.05)
        click()
        sleep(0.5)
        moveto(SELF_POSITION)
        sleep(0.05)
        clickright()

    def pickup(self, crop):
        moveto(SELF_POSITION)
        sleep(0.05)
        clickright()

        crop_image = "./common/samples/produce/" + crop + ".png"
        pos = [0, 0]
        while pos[0] != -1:
            moveto((400, 600))
            sleep(0.05)
            pos = imagesearcharea(crop_image, self.GRABREGION[0], self.GRABREGION[1], self.GRABREGION[2], self.GRABREGION[3], precision=0.7)
            
            if pos[0] == -1:
                break

            pos = (pos[0] + self.GRABREGION[0], pos[1] + self.GRABREGION[1])
            self._getdrop(pos)