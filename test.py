from ctypes import *
from time import sleep
from inputcontrol import *
from pyautogui import *

print(KEY_NAMES)

windll.user32.BlockInput(True)

sleep(2)
moveto((400, 400))
sleep(2)

windll.user32.BlockInput(False)
