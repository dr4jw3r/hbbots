import logging
import re
#
from os import listdir
from threading import Thread
from time import sleep, time
from cv2 import imread
#
from lib.ocr import OCR
from lib.imagesearch import imagesearch_fromscreenshot_withtemplate
from lib.utils.PublisherThread import PublisherThread
from lib.utils.PausableThread import PausableThread

class CropMonitor(PublisherThread, PausableThread):
    def __init__(self, screenshot_thread):
        PublisherThread.__init__(self)
        PausableThread.__init__(self)
        self.thread.name == __class__.__name__

        self.OCR = OCR(screenshot_thread)
        self.screenshot_thread = screenshot_thread

        self.logger = logging.getLogger("hbbot.cropmonitor")
        
        self.box_size = (32, 32)
        self.positions = ["left", "mid", "right"]
        self.precisions = {
            "normal": { "left": 0.5, "mid": 0.5, "right": 0.55 },
            "harvestall": { "left": 0.5, "mid": 0.5, "right": 0.5 }
        }

        self.current_precisions = self.precisions["normal"]

        IMAGES_DIR = "./common/samples/produce/crops/"
        self.templates = self.__readimages(IMAGES_DIR)

    def __readimages(self, directory):
        templates = {}
        files = listdir(directory)
        
        for position in self.positions:
            templates[position] = []
            samples = [f for f in files if f.find(position) != -1]

            for sample in samples:
                image = imread(directory + sample, 0)
                position = position

                templates[position].append({ "image": image, "position": position })

        return templates

    def useprecisions(self, precisions):
        self.logger.debug("setting precisions: " + precisions)
        self.current_precisions = self.precisions[precisions]

    def scan(self):
        replant = [True] * len(self.positions)
        screenshot = self.screenshot_thread.croppedcoordinates(352, 320, 448, 352)

        if screenshot is None:
            return None

        for i in range(len(self.positions)):
            position = self.positions[i]
            templates = self.templates[position]

            x1 = self.box_size[0] * i
            x2 = (self.box_size[0] * i) + self.box_size[0]
            y2 = self.box_size[1]

            cropped = screenshot.crop((x1, 0, x2, y2))

            for template in templates:
                pos = imagesearch_fromscreenshot_withtemplate(template["image"], cropped, precision=self.current_precisions[position])
                if pos[0] != -1:
                    replant[i] = False
                    break

        return replant

    def run(self):
        self.logger.debug("started")
        super().run()

        while not self.cancellation_token.is_cancelled:
            if self.is_paused:
                sleep(0.2)
                continue

            replant = self.scan()

            if any(replant):
                self.notify({"replant": replant})

            sleep(1)

        self.logger.debug("stopped")
