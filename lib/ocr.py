import re
import pytesseract
import numpy as np

from lib.imagesearch import region_grabber

from PIL import Image, ImageOps
from time import sleep, time

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

class OCR(object):
    def __init__(self):
        self.COLOR_RED = [255, 130, 130]
        self.COLOR_BLUE = [130, 130, 255]
        self.COLOR_WHITE = [255, 255, 255]
        self.COLOR_BLACK = [0, 0, 0]
        self.COLOR_LOCATION = [248, 248, 219]
        self.COLOR_GREEN = [0, 255, 0]
        self.COLOR_LOG = [180, 255, 180]

    def _process_chat_image(self, image):
        image = image.convert("RGB")

        image_data = np.array(image)
        rgb_data = image_data[:,:,:3]

        condition = np.logical_or(rgb_data == self.COLOR_RED, rgb_data == self.COLOR_BLUE)

        mask_white = np.all(rgb_data != self.COLOR_RED, axis = -1)
        mask_black = np.all(condition, axis = -1)

        rgb_data[mask_white] = self.COLOR_WHITE
        rgb_data[mask_black] = self.COLOR_BLACK

        processed = Image.fromarray(rgb_data)
        return processed
        
    def _process_image(self, img, color):
        img = img.convert("RGB")
        data = np.array(img)
        rgb = data[:,:,:3]

        mask = np.all(rgb != color, axis=-1)
        data[mask] = self.COLOR_WHITE

        mask = np.all(rgb == color, axis=-1)
        data[mask] = self.COLOR_BLACK

        return Image.fromarray(data)

    def getlocation(self):
        screenshot = region_grabber((228, 571, 396, 595))
        screenshot = ImageOps.invert(screenshot)
        # screenshot.save("./locations/" + str(time()) + ".png")

        try:
            res = pytesseract.image_to_string(screenshot)

            if res.find('%') is not -1:
                # screenshot.save("./locations/" + "percentage_" + str(time()) + ".png")
                return None

            split = res.split("(")
            loc = split[0].strip()

            m = re.findall('\d+', split[1])
            coords = [int(m[-2]), int(m[-1])]

            return (loc, coords)
        except IndexError:
            # screenshot.save("./locations/" + "indexerror_" + str(time()) + ".png")
            return None

    def readchat(self, query):
        processed = self._process_chat_image(region_grabber((15, 125, 285, 150)))

        res = pytesseract.image_to_string(processed).lower()

        for q in query:
            if res.find(q.lower()) == -1:
                return None
        
        return res

    def reptime(self):
        img = region_grabber((12, 520, 400, 540))
        img = self._process_image(img, self.COLOR_GREEN)

        img.save("rep_proc.png")

        res = pytesseract.image_to_string(img)
        
        if len(res) > 0:
            result = re.findall("\d+", res)

            if len(result) > 0:
                seconds_to_rep = result[-1]
                return int(seconds_to_rep)

        return -1

    def inventoryfull(self):
        img = region_grabber((12, 505, 100, 540))
        img = img.convert("RGB")

        data = np.array(img)
        rgb = data[:,:,:3]
        
        mask = np.all(rgb != self.COLOR_LOG, axis=-1)
        data[mask] = self.COLOR_WHITE

        mask = np.all(rgb == self.COLOR_LOG, axis=-1)
        data[mask] = self.COLOR_BLACK

        img = Image.fromarray(data)
        # img.save("inventory.png")

        res = pytesseract.image_to_string(img)

        keywords = ["bag", "ful"]
        for kw in keywords:
            if res.find(kw) == -1:
                return False
            
        return True

    def checkexhausted(self):
        sleep(0.1)
        img = region_grabber((10, 520, 275, 540))
        img = self._process_image(img, self.COLOR_LOG)
        res = pytesseract.image_to_string(img).lower()
        
        keywords = ["item", "exhausted"]
        for kw in keywords:
            if res.find(kw) == -1:
                return False

        return True        

    def checkbreak(self):
        img = region_grabber((10, 500, 290, 540))
        img = self._process_image(img, self.COLOR_LOG)
        res = pytesseract.image_to_string(img).lower()
        keywords = ["hoe", "exh"]

        with open("hoe_break.txt", "a") as f:
            f.write(res)

        for kw in keywords:
            if res.find(kw) == -1:
                return False

        return True      