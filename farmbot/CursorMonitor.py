import logging
# 
from threading import Thread
from time import sleep, time
from cv2 import imread
# 
from lib.inputcontrol import position
from lib.imagesearch import imagesearch_fromscreenshot_withtemplate
from lib.utils.PublisherThread import PublisherThread
from lib.utils.PausableThread import PausableThread

class CursorMonitor(PublisherThread, PausableThread):
    def __init__(self, screenshot_thread, cancellation_token):
        PublisherThread.__init__(self)
        PausableThread.__init__(self, cancellation_token)

        self.screenshot_thread = screenshot_thread
        self.logger = logging.getLogger("hbbot.cursormonitor")
        self.template = imread("./common/samples/misc/cursor.png", 0)

        self.corner_offset = 10
        self.size = (50, 50)

        self.thread.name == __class__.__name__

    def run(self):
        self.logger.debug("started")
        super().run()

        while not self.cancellation_token.is_cancelled:
            cursor_position = position()
            corner = (cursor_position[0] - self.corner_offset, cursor_position[1] - self.corner_offset)
            screenshot = self.screenshot_thread.croppedsize(corner[0], corner[1], self.size[0], self.size[1])

            sword_pos = imagesearch_fromscreenshot_withtemplate(self.template, screenshot, precision=0.44)
            
            if sword_pos[0] != -1:
                self.notify()
                sleep(2)

            sleep(0.2)

        self.logger.debug("stopped")