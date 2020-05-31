from time import sleep
#
from lib.inputcontrol import moveto, keydown, keyup, rightdown, rightup
# 
from farmbot.scanner import Scanner
from farmbot.positions import Position, PLANTING_POSITIONS, TEST_BOX_POSITIONS

class Harvester(object):
    def __init__(self):
        self.scanner = Scanner()
        
    def startharvest(self):
        # place cursor over middle position
        self._movetoplantingposition("center")
        
        keydown("ctrlleft")
        rightdown()

    def harvestsingle(self, index, cancellation_token):
        keydown("ctrlleft")
        rightdown()

        crop_stage = 0
        while crop_stage is not -1:
            if cancellation_token.is_cancelled:
                break
            # hoe break
            self._movetoposition(PLANTING_POSITIONS[index])
            sleep(0.5)
            crop_stage = self.scanner.getcropstage(TEST_BOX_POSITIONS[index])

    def stopharvest(self):
        keyup("ctrlleft")
        rightup()

    def _movetoposition(self, position):
        moveto((position.x, position.y))

    def _movetoplantingposition(self, position):
        for pos in PLANTING_POSITIONS:
            if pos.description == position:
                moveto((pos.x, pos.y))
                return

        

