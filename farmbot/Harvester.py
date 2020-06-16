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
    def __init__(self, crop_monitor, hoe_monitor, health_monitor, ocr, state):
        self.logger = logging.getLogger("hbbot.harvester")
        self.crop_monitor = crop_monitor
        self.hoe_monitor = hoe_monitor
        self.health_monitor = health_monitor
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

    def harvestall(self, cancellation_token):
        self.hoe_monitor.subscribe(self.__hoecallback, { "cancellation_token": cancellation_token })
        self.health_monitor.subscribe(self.__healthcallback)

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

        self.health_monitor.unsubscribe(self.__healthcallback)
        self.hoe_monitor.unsubscribe(self.__hoecallback)
        self.stopharvest()

    def __hoecallback(self, payload, args):
        self.stopharvest()
        equiphoe(self.state.gethoeindex(), self.ocr)
        self.harvestall(args["cancellation_token"])

    def __healthcallback(self, payload, args):
        # extract this and share with farmbot
        if payload["health_ticked"]:
            equipweapon()
            t = KillAroundThread(self.ocr, singlescan=True, no_loot=True)
            t.join()
            sleep(0.1)
            equiphoe(self.state.gethoeindex(), self.ocr)

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
        
    def __movetoplantingposition(self, position):
        for pos in PLANTING_POSITIONS:
            if pos.description == position:
                moveto((pos.x, pos.y))
                return

        

