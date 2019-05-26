from threading import Thread
from inputcontrol import *
from imagesearch import imagesearch_loop
from pyautogui import position

class EquipItemThread(object):
    def __init__(self, itemname):
        self.CLICKOFFSET = 5

        thread = Thread(target=self.run, args=(), kwargs={'itemname': itemname})
        thread.daemon = True
        thread.start()
    
    def run(self, itemname):
        imagepath = "./common/samples/inventory/" + itemname + ".png"
        keypress("f6")
        cursorpos = position()
        pos = imagesearch_loop(imagepath, 0.1)
        inputdisable()
        moveto(pos, self.CLICKOFFSET)
        keydown("ctrlleft")
        click()
        keyup("ctrlleft")
        keypress("f6")
        moveto(cursorpos)
        inputenable()

        
    def stop(self):
        pass