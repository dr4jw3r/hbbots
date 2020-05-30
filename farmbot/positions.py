class Position(object):
    def __init__(self, x, y, description):
        self.x = x
        self.y = y
        self.description = description

PLANTING_POSITIONS = [
    Position(397, 337, "center"),
    Position(368, 335, "left"),
    Position(432, 336, "right")
]

TEST_BOX_SIZE = (35, 65)
TEST_BOX_POSITIONS = [
    Position(384, 296, "center"),
    Position(351, 296, "left"),
    Position(415, 296, "right")
]

DROP_BOX_SIZE = (40, 40)
DROP_BOX_POSITIONS = [
    Position(380, 315, "center"),
    Position(345, 315, "left"),
    Position(410, 315, "right")
]