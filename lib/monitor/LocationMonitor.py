import logging
#
from time import sleep
from threading import Thread
#
from lib.ocr import OCR
#

class LocationMonitor(object):
    def __init__(self, screenshot_thread, cancellation_token):
        self.screenshot_thread = screenshot_thread
        self.ocr = OCR(screenshot_thread)
        self.cancellation_token = cancellation_token
        self.logger = logging.getLogger("hbbot.locationmonitor")
        self.location = None
        self.coordinates = None

        self.thread = Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.name = __class__.__name__
        self.thread.start()

    def getlocation(self):
        return self.location

    def getcoordinates(self):
        return self.coordinates

    def run(self):
        self.logger.debug("started")
        
        while not self.cancellation_token.is_cancelled:
            location = self.ocr.getlocation()
            if location is not None:
                self.location = location[0]
                self.coordinates = location[1]

        self.logger.debug("stopped")
        
