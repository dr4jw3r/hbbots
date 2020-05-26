import imagesearch
import re
import pytesseract
import numpy as np

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

    def process_chat_image(self, image):
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
        

    def getlocation(self):    
        screenshot = imagesearch.region_grabber((228, 571, 396, 595))
        screenshot = ImageOps.invert(screenshot)
        # screenshot.save("./locations/" + str(time()) + ".png")

        try:
            res = pytesseract.image_to_string(screenshot)

            if res.find('%') is not -1:
                return None

            split = res.split("(")
            loc = split[0].strip()

            m = re.findall('\d+', split[1])
            coords = [int(m[-2]), int(m[-1])]

            return (loc, coords)
        except IndexError:
            return None

    def readchat(self, query):
        processed = self.process_chat_image(imagesearch.region_grabber((15, 125, 285, 150)))

        res = pytesseract.image_to_string(processed)

        for q in query:
            if res.find(q) == -1:
                return None
        
        return res