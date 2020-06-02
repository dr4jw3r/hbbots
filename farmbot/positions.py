class Position(object):
    def __init__(self, x, y, description=None):
        self.x = x
        self.y = y
        self.description = description

SELF_POSITION = (400, 280)
FARM_WPTS = [(101, 106)]
PLANTING_POSITIONS = [
    Position(397, 337, "center"),
    Position(368, 335, "left"),
    Position(432, 336, "right")
]
SCAN_CURSOR_POSITIONS = [
    Position(432, 336, "right"),
    Position(432, 336, "right"),
    Position(400, 600, "offscreen"),
]

TEST_BOX_SIZE = (32, 32)
TEST_BOX_POSITIONS = [
    Position(384, 320, "center"),
    Position(352, 320, "left"),
    Position(416, 320, "right")
]

DROP_BOX_SIZE = (40, 40)
DROP_BOX_POSITIONS = [
    Position(380, 315, "center"),
    Position(345, 315, "left"),
    Position(410, 315, "right")
]

ENEMY_SCAN_POSITIONS = [
    Position(367, 260),
    Position(397, 260),
    Position(430, 260),
    Position(433, 305),
    Position(433, 333),
    Position(396, 333),
    Position(367, 330),
    Position(367, 300)
]