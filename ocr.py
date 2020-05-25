import imagesearch
import re
import pytesseract
import numpy as np

from PIL import Image, ImageOps
from time import sleep, time

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

COLOR_RED = [255, 130, 130]
COLOR_BLUE = [130, 130, 255]
COLOR_WHITE = [255, 255, 255]
COLOR_BLACK = [0, 0, 0]
COLOR_LOCATION = [248, 248, 219]

def process_chat_image(image):
    image = image.convert("RGB")

    image_data = np.array(image)
    rgb_data = image_data[:,:,:3]

    condition = np.logical_or(rgb_data == COLOR_RED, rgb_data == COLOR_BLUE)

    mask_white = np.all(rgb_data != COLOR_RED, axis = -1)
    mask_black = np.all(condition, axis = -1)

    rgb_data[mask_white] = COLOR_WHITE
    rgb_data[mask_black] = COLOR_BLACK

    processed = Image.fromarray(rgb_data)
    return processed
    

def getlocation():    
    screenshot = imagesearch.region_grabber((228, 571, 396, 595))
    screenshot = screenshot.quantize(colors=4, method=2)
    
    screenshot = screenshot.convert("RGB")
    data = np.array(screenshot)
    rgb = data[:,:,:3]

    mask = np.all(rgb != COLOR_LOCATION, axis = -1)
    data[mask] = COLOR_WHITE

    mask = np.all(rgb == COLOR_LOCATION, axis = -1)
    data[mask] = COLOR_BLACK

    screenshot = Image.fromarray(data)

    try:
        res = pytesseract.image_to_string(screenshot)

        if res.find('%') is not -1:
            return None

        split = res.split("(")
        loc = split[0].strip()

        m = re.findall('\d+', split[1])
        coords = [m[-2], m[-1]]

        return (loc, coords)
    except IndexError:
        return None

def readchat(query):
    processed = process_chat_image(imagesearch.region_grabber((0, 95, 255, 255)))

    processed.save("test.png")

    res = pytesseract.image_to_string(processed)

    for q in query:
        if res.find(q) == -1:
            return None
    
    return res