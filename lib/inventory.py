from lib.imagesearch import imagesearch_numLoop, imagesearcharea
from lib.inputcontrol import keypress

INVENTORY_IMAGE = "./common/samples/inventory/inventory.png"
INVENTORY_WINDOW_SIZE = (270, 207)

CORNER_OFFSET = (-99, -5)
DEFAULT_POSITION_OFFSET = (75, 75)
WEAPONS_OFFSET = (22, 182)

DISENCHANT_OFFSET = 6

# needs to be odd
DISENCHANT_STEPS = 5

def _addoffset(pos, offset):
    return (pos[0] + offset[0], pos[1] + offset[1])

def _findcorner():
    text_pos = imagesearch_numLoop(INVENTORY_IMAGE, 0.1, 5)
    
    if text_pos[0] is not -1:
        return _addoffset(text_pos, CORNER_OFFSET)

    return None

def defaultposition():
    return _addoffset(_findcorner(), DEFAULT_POSITION_OFFSET)

def wandposition():
    WAND_OFFSET = 20
    corner = _findcorner()
    x1 = corner[0] + (INVENTORY_WINDOW_SIZE[0] / 2)
    y1 = corner[1]

    x2 = x1 + (INVENTORY_WINDOW_SIZE[0] / 2)
    y2 = corner[1] + INVENTORY_WINDOW_SIZE[1]

    wand_pos = imagesearcharea("./common/samples/inventory/wand.png", x1, y1, x2, y2)
    wand_pos = (wand_pos[0] + x1, wand_pos[1] + y1)
    return (wand_pos[0] + WAND_OFFSET, wand_pos[1] + WAND_OFFSET)

def weaponsposition():
    return _addoffset(_findcorner(), WEAPONS_OFFSET)

def inventorypositions():
    start_offset = (int(DISENCHANT_STEPS / 2) * DISENCHANT_OFFSET)

    start = defaultposition()
    start = (start[0] - start_offset, start[1] - start_offset)

    positions = []

    for y in range(DISENCHANT_STEPS):
        for x in range(DISENCHANT_STEPS):
            x1 = start[0] + (DISENCHANT_OFFSET * x)
            y1 = start[1] + (DISENCHANT_OFFSET * y)
            positions.append((x1, y1))

    return positions

def openinventory():
    pos = imagesearch_numLoop(INVENTORY_IMAGE, 0.1, 5)
    
    if pos[0] is not -1:
        return
    else:
        keypress("f6")

def closeinventory():
    pos = imagesearch_numLoop(INVENTORY_IMAGE, 0.1, 5)
    
    if pos[0] is not -1:
        keypress("f6")
    else:
        return
