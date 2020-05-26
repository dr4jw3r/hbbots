import re
from time import sleep
from CancellationToken import CancellationToken
from threading import Thread
from ocr import OCR
from inputcontrol import keypress, keyup

class RepBotThread(object):
    def __init__(self):
        self.cancellation_token = CancellationToken()        
        self.OCR = OCR()

        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while not self.cancellation_token.is_cancelled:
            res = self.OCR.readchat(["trade", "rep"])
            if res is not None:
                if res.find(":") is not -1:
                    if res.find("]") is not -1:
                        split = res.split("]")
                    elif res.find(")") is not -1:
                        split = res.split(")")

                    split = split[1].split(":")
                    name = split[0].strip()
                    tr_string = "/traderep " + name
                    
                    # check functioning while killing

                    keyup("ctrlleft")
                    keyup("altleft")

                    keypress("enter")
                    for letter in tr_string:
                        keypress(letter)
                    keypress("enter")

            sleep(2)

    
    def stop(self):
        self.cancellation_token.cancel()