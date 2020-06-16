import logging
#
from time import sleep
# 
from lib.waypoints import WAYPOINTS
from lib.inputcontrol import moveto, click, leftdown, leftup, clickright, keydown, keyup, keypress
from lib.npc.common import clicknpc
from lib.buttons import buttonsellitems, buttonsell, buttonbuymisc, buttonseedbag, buttonquantitytens, buttonquantityunits, buttonpurchase
from lib.inventory import openinventory, closeinventory, defaultposition
from lib.imagesearch import imagesearch

logger = logging.getLogger("hbbot.shopkeeper")

def __gotoinsidelocation(movement):
    movement.followwaypoints(WAYPOINTS["shop_inside"])

def __clicksell(crop, scanner, cancellation_token):
    produce_pos = (0, 0)
    while produce_pos[0] != -1:
        if cancellation_token.is_cancelled:
            break

        produce_pos = scanner.findininventory(crop.name, precision=0.6)
        closeinventory()
        
        if produce_pos[0] != -1:
            shopkeeper_clicked = False
            
            while not shopkeeper_clicked:
                shopkeeper_clicked = clicknpc("shopkeeper", scanner, cancellation_token)
                sleep(0.1)

            buttonsellitems()
            moveto(produce_pos, 18, 18)
            sleep(0.1)
            click(18)
            sleep(0.1)
            buttonsell()
            sleep(0.1)

def __entersell(crop, scanner, cancellation_token):
    produce_pos = (0, 0)
    while produce_pos[0] != -1:
        produce_pos = scanner.findininventory(crop.name, precision=0.7)
        closeinventory()
        
        if produce_pos[0] != -1:
            shopkeeper_clicked = False
            
            while not shopkeeper_clicked:
                shopkeeper_clicked = clicknpc("shopkeeper", scanner, cancellation_token)
                sleep(0.1)
            
            buttonsellitems()
            moveto(produce_pos, 10, 10)
            sleep(0.1)
            click(2)
            sleep(0.1)
            keypress("enter")
            sleep(0.1)
            buttonsell()
            sleep(0.1)

def __scrolldown(amount):
    pos = imagesearch("./common/samples/buttons/scroll.png")
    moveto(pos, 5, 5)
    sleep(0.1)
    leftdown()
    sleep(0.1)
    moveto((pos[0], pos[1] + amount))
    sleep(0.1)
    leftup()
    sleep(0.1)

def __movebag():
    sleep(0.1)
    openinventory()
    pos = imagesearch("./common/samples/inventory/seed_bag.png", precision=0.7)

    if pos[0] != -1:
        moveto(pos, 5, 5)
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
    else:
        logger.error("bag position not found!")
        return False

    sleep(0.05)
    closeinventory()
    return True

def gotoshop(movement, scanner):
    waypoints = WAYPOINTS["shop"]
    movement.followwaypoints(waypoints, "shop")

    found = False
    while not found:
        sleep(1)
        pos = scanner.findnpc("shopkeeper")
        found = pos[0] != -1

        if not found:
            movement.followwaypoints([waypoints[-1]], 2, "shop")

def sellproduce(crop, scanner, cancellation_token):
    if crop.sell_mode == "click":
        __clicksell(crop, scanner, cancellation_token)
    elif crop.sell_mode == "enter":
        __entersell(crop, scanner, cancellation_token)

def buyseeds(crop, scanner, movement, cancellation_token):
    bag_moved = False

    while not bag_moved:
        clicked = False
        npc_clicked = False
        bag_moved = False
        while not clicked and not bag_moved:
            while not npc_clicked:
                npc_clicked = clicknpc("shopkeeper", scanner, cancellation_token)
                movement.gotolastwaypoint(WAYPOINTS["shop"], "shop")

            clicked = buttonbuymisc()
            __scrolldown(80)
            clicked = buttonseedbag(crop.name)

            if cancellation_token.is_cancelled:
                return

            bags_str = str(crop.num_bags)

            buttonquantitytens(int(bags_str[0]))

            if cancellation_token.is_cancelled:
                return

            buttonquantityunits(int(bags_str[1]))

            if cancellation_token.is_cancelled:
                return

            clicked = buttonpurchase()

            if cancellation_token.is_cancelled:
                return

            clickright()

            if cancellation_token.is_cancelled:
                return

            bag_moved = __movebag()

            if not bag_moved:
                closeinventory()
                __gotoinsidelocation(movement)