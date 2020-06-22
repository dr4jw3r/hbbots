from time import sleep
#
from lib.inputcontrol import moveto, keydown, leftdown, leftup, keyup
from lib.inventory import defaultposition
#

class InventoryManager(object):
    def __init__(self, scanner, crop, cancellation_token):
        self.scanner = scanner
        self.crop = crop
        self.cancellation_token = cancellation_token
    
    def moveproduce(self):
        pos = self.scanner.findininventory(self.crop.name, self.cancellation_token, 0.7)
        if pos[0] != -1:
            moveto(pos, self.crop.offset[0], self.crop.offset[1])
            sleep(0.2)
            keydown("shiftleft")
            sleep(0.2)
            leftdown()
            sleep(0.2)
            default_position = defaultposition()
            default_position = (default_position[0] + 50, default_position[1])
            moveto(default_position)
            sleep(0.2)
            leftup()
            sleep(0.2)
            keyup("shiftleft")
        
        sleep(0.2)