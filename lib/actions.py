from time import sleep
# 
from lib.spells import createfood
from lib.inputcontrol import clickright, moveto, click
from lib.inventory import openinventory, closeinventory, defaultposition

def eat(number, cancellation_token):
    for i in range(0, number):
        if cancellation_token.is_cancelled:
            return

        createfood(cancellation_token)
        sleep(0.2)
        click()
        sleep(0.2)
        
    openinventory()

    if cancellation_token.is_cancelled:
        return

    moveto(defaultposition())

    if cancellation_token.is_cancelled:
        return

    sleep(0.1)

    if cancellation_token.is_cancelled:
        return

    click(number * 2, 0.05)

    if cancellation_token.is_cancelled:
        return

    sleep(0.05)
    closeinventory()