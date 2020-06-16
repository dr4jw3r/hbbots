import logging
# 
from threading import Thread
from time import sleep, time
# 
from lib.ocr import OCR
from lib.utils.CancellationToken import CancellationToken
from lib.utils.PublisherThread import PublisherThread
from lib.utils.PausableThread import PausableThread

class HealthMonitor(PublisherThread, PausableThread):
    def __init__(self, ocr):
        PublisherThread.__init__(self)
        PausableThread.__init__(self)
        self.cancellation_token = CancellationToken()
        self.is_paused = False
        self.is_started = False
        self.ocr = ocr

        self.logger = logging.getLogger("hbbot.healthmonitor")

        self.thread.name == __class__.__name__

    def run(self):
        self.logger.debug("started")
        super().run()

        while not self.cancellation_token.is_cancelled:
            if self.cancellation_token.is_cancelled:
                    break

            if self.is_paused:
                sleep(0.2)
                continue

            if self.ocr.processhealth():
                self.notify({ "health_ticked": True })

            sleep(0.5)

        self.logger.debug("stopped")