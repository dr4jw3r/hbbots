from time import sleep
from threading import Thread
from imagesearch import imagesearch_loop, imagesearcharea, region_grabber
from inputcontrol import *

class AlchemyThread(object):
    def __init__(self):
        self.stopthread = False

        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def clickitem(self, pos):
        moveto(pos, 10)
        click(2, 0.05)
        sleep(1)

    def trynow(self):
        pos = imagesearch_loop("./common/samples/alch/trynow2.png", 0.1, 0.5)
        moveto(pos, 5)
        click()

    def finditem(self, im, itemname, precision=0.8):
        imagepath = "./common/samples/alch/" + itemname + ".png"

        pos = (-1, -1)

        while pos[0] == -1:
            pos = imagesearcharea(imagepath, 0, 0, 1920, 1080, precision, im)
            precision -= 0.05

        return pos

    def makemanapotion(self):
        im = region_grabber((0, 0, 1920, 1080))

        bowlpos = self.finditem(im, "alchemybowl")
        slimepos = self.finditem(im, "slimejelly")
        snakeskinpos = self.finditem(im, "snakeskin")
        antantennapos = self.finditem(im, "antantenna")

        self.clickitem(bowlpos)
        self.clickitem(slimepos)
        self.clickitem(snakeskinpos)
        self.clickitem(antantennapos)

        self.trynow()
        sleep(4)

    def run(self):
        while not self.stopthread:
            self.makemanapotion()

    def stop(self):
        self.stopthread = True