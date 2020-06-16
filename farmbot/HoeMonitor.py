import logging
# 
from threading import Thread
from time import sleep, time
from cv2 import imread
# 
from lib.inventory import getbounds
from lib.imagesearch import imagesearch_fromscreenshot_withtemplate
from lib.utils.CancellationToken import CancellationToken
from lib.utils.PublisherThread import PublisherThread
from lib.utils.PausableThread import PausableThread

class HoeMonitor(PublisherThread, PausableThread):
    def __init__(self, screenshot_thread, state):
        PublisherThread.__init__(self)
        PausableThread.__init__(self)

        self.screenshot_thread = screenshot_thread
        self.state = state
        self.logger = logging.getLogger("hbbot.hoemonitor")
        self.template = imread("./common/samples/inventory/hoe.png", 0)

        self.areas = [
            (225, 25, 270, 70),
            (225, 65, 270, 110),
            (225, 110, 270, 155),
            (225, 155, 270, 200),
        ]

        self.fade_delay = 10
        self.fade_timer = 0
        
        self.thread.name == __class__.__name__

    def run(self):
        self.logger.debug("started")
        super().run()

        while not self.cancellation_token.is_cancelled:
            elapsed = time() - self.fade_timer
            if self.is_paused or elapsed < self.fade_delay:
                sleep(0.2)
                continue

            b = getbounds()
            a = self.areas[self.state.gethoeindex()]
            
            x1 = b[0][0] + a[0]
            y1 = b[0][1] + a[1]
            x2 = b[0][0] + a[2]
            y2 = b[0][1] + a[3]

            screenshot = self.screenshot_thread.croppedcoordinates(x1, y1, x2, y2)
            pos = imagesearch_fromscreenshot_withtemplate(self.template, screenshot, precision=0.7)
            screenshot.save("hoe_area_{0}.png".format(self.state.gethoeindex()))

            if pos[0] != -1:
                self.state.incrementhoeindex()
                self.notify({ "hoe_index": self.state.gethoeindex() })

        self.logger.debug("stopped")