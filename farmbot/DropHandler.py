from cv2 import imread
from time import sleep, time
# 
from lib.imagesearch import imagesearch_fromscreenshot_withtemplate
from lib.inputcontrol import moveto, click, clickright
from lib.positions import SELF

class DropHandler(object):
    def __init__(self, crop, screenshot_thread):
        self.template = imread("./common/samples/produce/" + crop.name + ".png", 0)
        self.screenshot_thread = screenshot_thread
        self.region_corner = (300, 239)
        self.region_size = (194, 130)
        self.timeout = 10
        self.drop_precision = 0.7

    def __getdrop(self, pos, cancellation_token):
        moveto(pos)
        sleep(0.05)
        click()
        sleep(0.6)
        moveto(SELF["upper"])
        sleep(0.05)
        clickright()
        sleep(1)

    def pickup(self, cancellation_token):
        pos = (0, 0)
        timeout_timer = time()

        moveto(SELF["upper"])
        sleep(0.05)
        clickright()
        sleep(0.1)

        while pos[0] != -1:
            if cancellation_token.is_cancelled:
                break

            if time() - timeout_timer >= self.timeout:
                break

            moveto((400, 600))
            sleep(0.21)
            
            screenshot = self.screenshot_thread.croppedsize(self.region_corner[0], self.region_corner[1], self.region_size[0], self.region_size[1])
            pos = imagesearch_fromscreenshot_withtemplate(self.template, screenshot, precision=self.drop_precision)
            
            if pos[0] == -1:
                break

            pos = (pos[0] + self.region_corner[0], pos[1] + self.region_corner[1])
            self.__getdrop(pos, cancellation_token)

            if cancellation_token.is_cancelled:
                break