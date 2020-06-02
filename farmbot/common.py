from time import sleep, time
##########
from lib.common import clicknpc, clickbutton, followwpts
from lib.imagesearch import imagesearch_numLoop, imagesearcharea
from lib.inputcontrol import moveto, click, clickright, keypress, keydown, keyup, leftdown, leftup, rightdown, rightup, position
from lib.inventory import openinventory, closeinventory, hoepositions, defaultposition, getbounds
from lib.ocr import OCR
from farmbot.positions import FARM_WPTS
from pyautogui import screenshot

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

    # return whether hoe equipped
    return not is_exhausted

def gotofarm_fromrecall(cancellation_token):    
    followwpts(cancellation_token, FARM_WPTS, tolerance=0)

def buyseeds(seeds, amount=24, cancellation_token=None):
    clicknpc("shopkeeper", cancellation_token)
    clickbutton("buy_misc_shop", cancellation_token)
    scrolldown()
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

def scrolldown():
    sleep(0.1)
    pos = imagesearch_numLoop("./common/samples/buttons/scroll.png", 0.1, 5)
    moveto(pos, 5, 5)
    sleep(0.1)
    leftdown()
    sleep(0.1)
    moveto((pos[0], pos[1] + 80))
    sleep(0.1)
    leftup()
    sleep(0.1)

def sellproduce(produce, sell_mode, cancellation_token):
    # Open Inventory and take a screenshot!
    openinventory()
    sleep(0.05)
    screenshot().save("./sales/{0}.png".format(time()))
    closeinventory()
    sleep(0.05)

    if sell_mode == "click":
        produce_pos = (0, 0)
        while produce_pos[0] != -1:
            if cancellation_token.is_cancelled:
                break

            openinventory()
            sleep(0.05)
            produce_pos = imagesearch_numLoop("./common/samples/inventory/" + produce + ".png", 0.1, 5, precision=0.65)
            closeinventory()

            if produce_pos[0] == -1:
                break

            clicknpc("shopkeeper", cancellation_token)
            clickbutton("sell_items_store", cancellation_token)
            moveto(produce_pos, 18)
            click(18, 0.02)

            # If any items to be sold - click button
            sell_button_pos = imagesearch_numLoop("./common/samples/buttons/sell_items_btn.png", 0.1, 10)
            moveto(sell_button_pos, 10)
            sleep(0.1)
            click()
            sleep(1)

    elif sell_mode == "enter":
        clicknpc("shopkeeper", cancellation_token)
        clickbutton("sell_items_store", cancellation_token)

        produce_pos = imagesearch_numLoop("./common/samples/inventory/" + produce + ".png", 0.1, 5)
        moveto(produce_pos, 10)
        sleep(0.1)
        click(2)
        sleep(0.1)
        keypress("enter")

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
    gotofarm_fromrecall(cancellation_token)