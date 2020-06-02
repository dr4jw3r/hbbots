from time import sleep
from threading import Thread
from lib.CancellationToken import CancellationToken
from lib.ocr import OCR

class LocationMonitor(object):
    def __init__(self):
        self.ocr = OCR()
        self.cancellation_token = CancellationToken()
        self.location = None
        self.coordinates = None

        self.thread = Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def getlocation(self):
        return self.location

    def getcoordinates(self):
        return self.coordinates

    def run(self):
        while not self.cancellation_token.is_cancelled:
            location = self.ocr.getlocation()

            if location is not None:
                self.location = location[0]
                self.coordinates = location[1]

            sleep(1)

    def stop(self):
        self.cancellation_token.cancel()
