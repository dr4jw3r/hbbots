from time import sleep
# 
from lib.imagesearch import imagesearch_fromscreenshot
from lib.inventory import getbounds

class Scanner(object):
    def __init__(self, screenshot_thread, cancellation_token):
        self.screenshot_thread = screenshot_thread
        self.cancellation_token = cancellation_token

    def findnpc(self, npc, precision=0.8):
        scr = self.screenshot_thread.screenshot
        pos = imagesearch_fromscreenshot("./common/samples/monsters/{0}.png".format(npc), scr, precision)
        return (pos, pos[0] != -1)

    def findininventory(self, item, precision=0.8):
        b = getbounds(self.cancellation_token)
        sleep(0.25)
        scr = self.screenshot_thread.croppedcoordinates(b[0][0], b[0][1], b[1][0], b[1][1])
        pos = imagesearch_fromscreenshot("./common/samples/inventory/{0}.png".format(item), scr, precision)

        if pos[0] == -1:
            return (-1, -1)
        else:
            pos = (pos[0] + b[0][0], pos[1] + b[0][1])
            return pos
