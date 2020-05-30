from lib.inputcontrol import moveto, keydown, keyup, rightdown, rightup
# 
from farmbot.positions import Position, PLANTING_POSITIONS

class Harvester(object):
    def __init__(self):
        pass
        
    def startharvest(self):
        # place cursor over middle position
        self._movetoplantingposition("center")

    def _movetoplantingposition(self, position):
        for pos in PLANTING_POSITIONS:
            if pos.description == position:
                moveto((pos.x, pos.y))
                return

        

