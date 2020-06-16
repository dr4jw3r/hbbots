from time import sleep
# 
from lib.imagesearch import imagesearch
from lib.inputcontrol import moveto, click
# 

def __clickbutton(button, offset_x, offset_y, num_clicks=1):
    moveto((0, 0))
    sleep(0.05)
    pos = imagesearch("./common/samples/buttons/" + button + ".png")

    if pos[0] != -1:
        moveto(pos, offset_x, offset_y)
        sleep(0.1)
        click(num_clicks)
        sleep(0.5)
        return True

    return False

def buttonrepairall():
    return __clickbutton("repair_all", 10, 10)

def buttonrepair():
    return __clickbutton("repair", 10, 10)

def buttonsellitems():
    return __clickbutton("sell_items_store", 10, 10)

def buttonsell():
    return __clickbutton("sell_items_btn", 10, 10)

def buttonbuymisc():
    return __clickbutton("buy_misc_shop", 10, 10)

def buttonseedbag(crop_name):
    return __clickbutton("seed_bag_{0}".format(crop_name), 5, 5)

def buttonquantitytens(num):
    return __clickbutton("quantity_selector", 5, 5, num)

def buttonquantityunits(num):
    num -= 1
    if num < 0:
        num = 0
        
    return __clickbutton("quantity_selector", 20, 5, num)

def buttonpurchase():
    return __clickbutton("purchase", 5, 5)