from time import sleep, time
#
from lib.inputcontrol import moveto, keydown, keyup, rightdown, rightup
# 
from farmbot.scanner import Scanner
from farmbot.positions import Position, PLANTING_POSITIONS, TEST_BOX_POSITIONS
# 
from farmbot.common import equiphoe

class Harvester(object):
    def __init__(self):
        self.scanner = Scanner()
        
    def startharvest(self):
        # place cursor over middle position
        self._movetoplantingposition("center")
        
        rightdown()

    def hoe(self, index):
        hoe_equipped = False
        while not hoe_equipped:
            hoe_equipped = equiphoe(index)

            if not hoe_equipped:
                index += 1

        return index

    def harvestsingle(self, index, hoe_thread, hoe_index, cancellation_token):
        timeout = 35
        crop_stage = 0
        
        start_time = time()
        while crop_stage is not -1:
            rightdown()

            if cancellation_token.is_cancelled:
                break
            
            if hoe_thread.ishoebroken():
                rightup()
                hoe_index = self.hoe(hoe_index)
                hoe_thread.acknowledge()

            self._movetoposition(PLANTING_POSITIONS[index])
            sleep(1)
            
            moveto((400, 600))
            sleep(0.05)
            crop_stage = self.scanner.getcropstageold(TEST_BOX_POSITIONS[index])

            if time() - start_time >= timeout:
                print("TIMED OUT")
                return

    def stopharvest(self):
        rightup()

    def _movetoposition(self, position):
        moveto((position.x, position.y))

    def _movetoplantingposition(self, position):
        for pos in PLANTING_POSITIONS:
            if pos.description == position:
                moveto((pos.x, pos.y))
                return

        

