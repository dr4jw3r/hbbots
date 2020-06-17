import logging
#
from time import sleep
# 
from lib.inputcontrol import moveto, rightdown, rightup
from lib.equipment import equiphoe, equipweapon
from lib.threads.killaround import KillAroundThread
# 
from farmbot.positions import PLANTING_POSITIONS
# 

class Harvester(object):
    def __init__(self, crop_monitor, ocr, state):
        self.logger = logging.getLogger("hbbot.harvester")
        self.crop_monitor = crop_monitor
        self.ocr = ocr
        self.state = state

    def startharvest(self):        
        self.logger.debug("start harvest")
        self.__movetoplantingposition("center")
        sleep(0.1)
        rightdown()
        sleep(0.05)
 
    def stopharvest(self):        
        self.logger.debug("stop harvest")
        rightup()
        sleep(0.1)

    def harvestall(self, replant, cancellation_token):
        replant = self.crop_monitor.scan()
        needs_harvest = [False] * len(replant)
        
        for i in range(len(replant)):
            needs_harvest[i] = not replant[i]

        if any(needs_harvest):
            self.startharvest()

        order = [1, 0, 2]
        for i in order:
            if needs_harvest[i]:
                self.__harvestsingle(i, cancellation_token)

        self.stopharvest()

    def __harvestsingle(self, index, cancellation_token):
        position = PLANTING_POSITIONS[index]
        has_crop = True        

        if cancellation_token.is_cancelled:
            return

        moveto((position.x, position.y))
        sleep(0.5)
        has_crop = self.crop_monitor.scansingle(index)

        if has_crop:
            self.__harvestsingle(index, cancellation_token)                    
        
    def moveto(self, index):
        position = PLANTING_POSITIONS[index]
        print("moving to", position.description)
        self.__movetoplantingposition(position.description)

    def __movetoplantingposition(self, position):
        for pos in PLANTING_POSITIONS:
            if pos.description == position:
                moveto((pos.x, pos.y))
                return

        

