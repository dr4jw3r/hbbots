import logging
# 
from threading import Thread
from time import sleep, time
# 
from lib.ocr import OCR
from lib.utils.PublisherThread import PublisherThread
from lib.utils.PausableThread import PausableThread

class BagMonitor(PublisherThread, PausableThread):
    def __init__(self, ocr, scanner, cancellation_token):
        PublisherThread.__init__(self)
        PausableThread.__init__(self, cancellation_token)
        self.is_paused = False
        self.is_started = False
        self.ocr = ocr
        self.scanner = scanner
        
        self.logger = logging.getLogger("hbbot.bagmonitor")

        self.thread = Thread(target=self.run, args=())
        self.thread.name = __class__.__name__
        self.thread.daemon = True

    def run(self):
        self.logger.debug("started")
        super().run()

        while not self.cancellation_token.is_cancelled:
            if self.is_paused:
                sleep(0.2)
                continue

            pos = self.scanner.findininventory("seed_bag", precision=0.65)
            if pos[0] == -1:
                self.notify({ "has_bag": False })
            sleep(0.2)

        self.logger.debug("stopped")