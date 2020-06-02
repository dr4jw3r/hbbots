from time import sleep, time
from lib.inputcontrol import moveto, click, clickright
from lib.imagesearch import imagesearcharea
from farmbot.positions import SELF_POSITION

class DropHandler(object):
    def __init__(self):
        self.GRABREGION = (319, 222, 481, 383)

    def _getdrop(self, pos, cancellation_token):
        if cancellation_token.is_cancelled:
            return

        moveto(pos)
        sleep(0.05)
        click()

        if cancellation_token.is_cancelled:
            return

        sleep(0.5)

        if cancellation_token.is_cancelled:
            return

        moveto(SELF_POSITION)
        sleep(0.1)
        clickright()

    def pickup(self, crop, cancellation_token):
        TIMEOUT = 15
        crop_image = "./common/samples/produce/" + crop + ".png"
        pos = [0, 0]

        timeout_timer = time()
        while pos[0] != -1:
            if cancellation_token.is_cancelled:
                break

            if time() - timeout_timer >= TIMEOUT:
                break

            moveto((400, 600))
            sleep(0.05)
            pos = imagesearcharea(crop_image, self.GRABREGION[0], self.GRABREGION[1], self.GRABREGION[2], self.GRABREGION[3], precision=0.95)
            
            if pos[0] == -1:
                break

            pos = (pos[0] + self.GRABREGION[0], pos[1] + self.GRABREGION[1])
            self._getdrop(pos, cancellation_token)

            if cancellation_token.is_cancelled:
                break