from time import sleep
#
from lib.inputcontrol import moveto, keydown, leftdown, leftup, keyup
from lib.inventory import defaultposition
#

class InventoryManager(object):
    def __init__(self, scanner, crop):
        self.scanner = scanner
        self.crop = crop
    
    def moveproduce(self):
        pos = self.scanner.findininventory(self.crop.name, 0.7)
        if pos[0] != -1:
            moveto(pos, 10, 10)
            sleep(0.1)
            keydown("shiftleft")
            sleep(0.1)
            leftdown()
            sleep(0.1)
            default_position = defaultposition()
            default_position = (default_position[0] + 50, default_position[1])
            moveto(default_position)
            sleep(0.1)
            leftup()
            sleep(0.1)
            keyup("shiftleft")
        
        sleep(0.1)