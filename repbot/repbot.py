import re

from time import sleep, time

from threading import Thread

from lib.CancellationToken import CancellationToken
from lib.ocr import OCR
from lib.inputcontrol import keypress, keyup

class RepBotThread(object):
    def __init__(self):
        self.cancellation_token = CancellationToken()        
        self.OCR = OCR()
        self.reptime = -1        

        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        rep_checked = 0

        while not self.cancellation_token.is_cancelled:
            sleep(1)


            if self.reptime == -1:
                self.sendmessage("/checkrep")
                sleep(1)
                self.reptime = self.OCR.reptime()
                rep_checked = time()

            elif self.reptime > 0:
                if self.cancellation_token.is_cancelled:
                    return
                
                # set time until recheck rep
                elapsed = time() - rep_checked
                if int(elapsed) >= self.reptime:
                    self.reptime = -1

            elif self.reptime == 0:
                if self.cancellation_token.is_cancelled:
                    return

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
                        self.sendmessage(tr_string)
                        self.reptime = -1
                        sleep(10)

            

    def sendmessage(self, message):
        # Release these keys just in case they were down
        keyup("ctrlleft")
        keyup("altleft")

        keypress("enter")
        for letter in message:
            keypress(letter)
        keypress("enter")

    def stop(self):
        self.cancellation_token.cancel()