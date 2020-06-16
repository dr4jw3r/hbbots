from time import sleep
#
from lib.positions import SELF
from lib.inputcontrol import moveto, click
from lib.threads.CastSpellThread import CastSpellThread
#

def recall(cancellation_token):
    if cancellation_token.is_cancelled:
        return

    CastSpellThread("recall")
    sleep(2)
    moveto(SELF["top"])
    sleep(0.1)

    if cancellation_token.is_cancelled:
        return

    click()
    sleep(1)

def createfood(cancellation_token):
    if cancellation_token.is_cancelled:
        return

    CastSpellThread("createfood")
    sleep(2)
    moveto(SELF["upper"])
    sleep(0.1)

    if cancellation_token.is_cancelled:
        return

    click()
    sleep(0.1)