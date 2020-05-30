from time import sleep, time
##########
from lib.common import clicknpc, clickbutton, followwpts
from lib.imagesearch import imagesearch_numLoop, imagesearcharea
from lib.inputcontrol import moveto, click, clickright, keypress, keydown, keyup, leftdown, leftup, rightdown, rightup, position
from lib.inventory import openinventory, closeinventory, hoepositions, defaultposition, getbounds
from lib.ocr import OCR

FARM_WPTS = [(95, 99)]
SELF_POSITION = (400, 280)
PLANTING_POSITIONS = [
    (397, 337),
    (368, 335),
    (432, 336)
]
RETURN_POSITIONS = [
    [(370, 267), (433, 301)],
    [(429, 272)],
    [(366, 270)]
]

DROP_BOX_SIZE = (40, 40)
DROP_CHECK_POSITIONS = [
    (380, 315),
    (345, 315),
    (410, 315)
]

TEST_BOX_SIZE = (35, 65)
TEST_BOXES = [
    (384, 296),
    (351, 296),
    (415, 296)
]

OCR = OCR()

def _teststage(pos, planting_pos):
    moveto((0, 0))
    sleep(0.2)

    x2 = pos[0] + TEST_BOX_SIZE[0]
    y2 = pos[1] + TEST_BOX_SIZE[1]

    stage = -1
    crop_pos = (-1, -1)

    for s in range(1, 4):
        for i in range(3):
            crop_pos = imagesearcharea("./common/samples/produce/crop_" + str(s) + ".png", pos[0], pos[1], x2, y2, 0.45)

            if crop_pos[0] != -1:
                stage = s
                break
            
            sleep(0.05)
    
    moveto(planting_pos)

    return stage

def _stopharvest():
    rightup()
    keyup("ctrlleft")

def harvest(cancellation_token, crop_type):
    for i in range(3):
        if cancellation_token.is_cancelled:
            _stopharvest()
            return
        
        test_time = 0
        test_pos = TEST_BOXES[i]
        planting_pos = PLANTING_POSITIONS[i]
        return_positions = RETURN_POSITIONS[i]
        drop_position = DROP_CHECK_POSITIONS[i]

        start_time = time()
        
        crop_stage = 0
        moveto(planting_pos)
        sleep(0.1)

        while not crop_stage == -1:
            if cancellation_token.is_cancelled:
                _stopharvest()
                return

            keydown("ctrlleft")
            rightdown()

            sleep(1)

            if cancellation_token.is_cancelled:
                _stopharvest()
                return

            # every x seconds test for last stage of plant
            if time() - start_time >= test_time:
                rightup()
                keyup("ctrlleft")
                crop_stage = _teststage(test_pos, planting_pos)

                if crop_stage == 3:
                    test_time = 1.5
                elif crop_stage == 2:
                    test_time = 5
                elif crop_stage == 1:
                    test_time = 15

                start_time = time()

            else:
                # check for break of hoe
                if checkhoebreak():
                    _stopharvest()
                    return

        if cancellation_token.is_cancelled:
            _stopharvest()
            return        

        if isdrop(drop_position, planting_pos, crop_type):
            moveto(planting_pos)
            sleep(0.1)
            click()
            sleep(0.2)
            moveto(SELF_POSITION)
            sleep(0.1)
            clickright()
            sleep(0.05)
        
            for rp in return_positions:
                moveto(rp)
                sleep(0.1)
                click()

            sleep(0.05)
            click()

        if cancellation_token.is_cancelled:
            _stopharvest()
            return

    moveto(SELF_POSITION)
    sleep(0.1)
    clickright()
    sleep(0.1)

def checkhoebreak():
    return OCR.checkbreak()    

def isdrop(position, cursor_position, produce):
    moveto((0, 0))
    sleep(0.1)
    image = "./common/samples/produce/" + produce + ".png"
    drop_position = imagesearcharea(image, position[0], position[1], position[0] + DROP_BOX_SIZE[0], position[1] + DROP_BOX_SIZE[1], precision=0.55)
    moveto(cursor_position)
    if drop_position[0] is not -1:
        return True
    else:
        return False

def plantseeds(cancellation_token):
    has_planted = False
    openinventory()    
    b = getbounds()    

    for pos in PLANTING_POSITIONS:
        if cancellation_token.is_cancelled:
            break

        sleep(0.08)
        seed_bag_pos = imagesearcharea("./common/samples/inventory/seed_bag.png", b[0][0], b[0][1], b[1][0], b[1][1], 0.7)

        if seed_bag_pos[0] == -1:
            continue

        seed_bag_pos = (seed_bag_pos[0] + b[0][0], seed_bag_pos[1] + b[0][1])

        moveto(seed_bag_pos, 5, 5)
        sleep(0.1)
        click(2)
        sleep(0.1)
        moveto(pos)
        sleep(0.1)
        click()
        has_planted = True

    closeinventory()
    sleep(0.05)
    return has_planted

def equiphoe(hoe_index):
    openinventory()
    sleep(0.05)

    try:
        hoe_pos = hoepositions()[hoe_index]
    except IndexError:
        return False

    if hoe_pos[0] != -1:
        moveto(hoe_pos)
        sleep(0.1)
        click(2)

        is_exhausted = OCR.checkexhausted()

    closeinventory()
    # return whether hoe equipped
    return not is_exhausted

def gotofarm_fromrecall(cancellation_token):    
    followwpts(cancellation_token, FARM_WPTS, tolerance=0)

def buyseeds(seeds, amount=24, cancellation_token=None):
    clicknpc("shopkeeper", cancellation_token)
    clickbutton("buy_misc_shop", cancellation_token)
    clickbutton("seed_bag_" + seeds, cancellation_token)
    
    amount_str = str(amount)
    
    # tens
    for i in range(int(amount_str[0])):
        clickbutton("quantity_selector", cancellation_token, 5, 5)

    # units
    u = int(amount_str[1]) - 1
    if u > 0:
        for i in range(u):
            clickbutton("quantity_selector", cancellation_token, 20, 5)

    clickbutton("purchase", cancellation_token, 5, 5)
    clickright()

def sellproduce(produce, cancellation_token):
    clicknpc("shopkeeper", cancellation_token)
    clickbutton("sell_items_store", cancellation_token)

    produce_pos = imagesearch_numLoop("./common/samples/inventory/" + produce + ".png", 0.1, 5, precision=0.7)

    print(produce_pos)

    moveto(produce_pos, 10)
    sleep(0.1)
    click(40, 0.02)
    sleep(0.1)

    # If any items to be sold - click button
    sell_button_pos = imagesearch_numLoop("./common/samples/buttons/sell_items_btn.png", 0.1, 10)
    moveto(sell_button_pos, 10)
    sleep(0.1)
    click()
    sleep(1)

    # If no items to be sold, close the list
    sell_list_pos = imagesearch_numLoop("./common/samples/misc/sell_list.png", 0.1, 5)
    if sell_list_pos[0] != -1:
        moveto(sell_list_pos)
        sleep(0.5)
        clickright()
        sleep(0.5)

    closeinventory()

def moveseeds(cancellation_token):
    openinventory()
    seed_bag_pos = imagesearch_numLoop("./common/samples/inventory/seed_bag.png", 0.1, 5)
    moveto(seed_bag_pos, 5, 5)
    sleep(0.1)
    keydown("shiftleft")
    sleep(0.1)
    leftdown()
    sleep(0.1)
    default_position = defaultposition()
    default_position = (default_position[0], default_position[1] + 50)
    moveto(default_position)
    sleep(0.1)
    leftup()
    sleep(0.1)
    keyup("shiftleft")

def verifylocation(cancellation_token):
    loc = OCR.getlocation()

    print(loc)

    if loc is not None:
        c = loc[1]

        if c[0] != FARM_WPTS[0] or c[1] != FARM_WPTS[1]:
            gotofarm_fromrecall(cancellation_token)