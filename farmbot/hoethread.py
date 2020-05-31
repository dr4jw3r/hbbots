from threading import Thread
from time import sleep
from lib.ocr import OCR
from lib.CancellationToken import CancellationToken

class HoeThread(object):
    def __init__(self):
        self.OCR = OCR()
        self.cancellation_token = CancellationToken()
        self.hoe_break = False

        self.thread = Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        sleep(5)
        
        while not self.cancellation_token.is_cancelled:
            broken = self.OCR.checkbreak()

            if broken:
                self.hoe_break = True
                sleep(5)

            sleep(0.5)

    def ishoebroken(self):
        return self.hoe_break

    def acknowledge(self):
        self.hoe_break = False

    def stop(self):
        self.cancellation_token.cancel()
    