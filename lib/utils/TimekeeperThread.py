import logging
# 
from threading import Thread
from time import sleep, time
# 

class TimekeeperThread(object):
    def __init__(self, cancellation_token):
        self.cancellation_token = cancellation_token

        self.logger = logging.getLogger("hbbot.timekeeper")

        self.timer = 0
        self.__registrations = []
        self.started = False
        self.paused = False

        self.thread = Thread(target=self.run, args=())
        self.thread.daemon = True

    def __checkregistrations(self):
        for registration in self.__registrations:
            if self.timer - registration["timer"] >= registration["interval"]:
                registration["callback"]()
                registration["timer"] = self.timer

    def start(self):
        for registration in self.__registrations:
            registration["timer"] = time()

        if not self.started:
            self.thread.start()
            self.started = True

    def pause(self):
        self.paused = True

    def stop(self):
        self.cancellation_token.cancel()
    
    def join(self):
        if self.started:
            self.thread.join()

    def register(self, callback, time):
        self.__registrations.append({ "callback": callback, "interval": time, "timer": 0})

    def reset(self):
        for registration in self.__registrations:
            registration["timer"] = time()

        self.paused = False

    def run(self):
        self.logger.debug("started")

        while not self.cancellation_token.is_cancelled:
            sleep(0.5)

            if not self.paused:
                self.__checkregistrations()
                self.timer = time()

        self.logger.debug("stopped")
