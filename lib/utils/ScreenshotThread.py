import logging
#
from time import sleep
from threading import Thread
from pyautogui import screenshot
# 

class ScreenshotThread(object):
    def __init__(self, cancellation_token):
        self.screenshot = None
        self.cancellation_token = cancellation_token
        self.logger = logging.getLogger("hbbot.screenshotthread")

        self.INTERVAL = 0.2

        self.thread = Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.name = __class__.__name__
        self.thread.start()

    def run(self):
        self.logger.debug("started")

        while not self.cancellation_token.is_cancelled:
            self.screenshot = screenshot()
            sleep(self.INTERVAL)
        
        self.logger.debug("stopped")

    def stop(self):
        self.cancellation_token.cancel()

    def join(self):
        self.thread.join()

    def croppedcoordinates(self, x1, y1, x2, y2):
        if self.screenshot is not None:
            return self.screenshot.crop((x1, y1, x2, y2))
        return None

    def croppedsize(self, x1, y1, w, h):
        if self.screenshot is not None:
            return self.screenshot.crop((x1, y1, x1 + w, y1 + h))
        return None