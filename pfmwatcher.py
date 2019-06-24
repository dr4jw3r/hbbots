from threading import Thread
from imagesearch import imagesearch
from time import sleep

class PfmWatcherThread(object):
    def __init__(self):
        self.keeprunning = True

        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def castpfm(self):
        pass

    def run(self):
        while self.keeprunning:
            self.castpfm()

    def stop(self):
        print("Stopping")