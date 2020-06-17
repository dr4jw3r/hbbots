import threading
import winsound

from time import sleep
from system_hotkey import SystemHotkey

from lib.inputcontrol import rightdown, rightup, position

from lib.threads.killaround import KillAroundThread
from lib.threads.CastSpellThread import CastSpellThread
from lib.threads.adbot import AdThread
from lib.threads.alchbot import AlchemyThread
from lib.threads.equipitem import EquipItemThread
from lib.threads.fakeamp import FakeAmpThread
from lib.threads.mpregen import MpRegenThread
from lib.threads.clicker import ClickerThread

#
from lib.utils.ScreenshotThread import ScreenshotThread
from lib.ocr import OCR
from lib.utils.CancellationToken import CancellationToken
#

from orcbot.orcbot import OrcThread
from levelbot.levelbot import LevellingBotThread
from repbot.repbot import RepBotThread

from farmbot.farmbot import FarmThread
from farmbot.Crop import Crop

class HotkeyHandler():
    def __init__(self):
        self.repthread = None
        self.farmthread = None
        self.currentthread = None
        self.mpregenbotthread = None
        self.clickerthread = None
        self.alchemypositions = [None] * 7
        self.currentshield = "lagishield"

        self.st = None
        self.ocr_temp = None

    def handlehotkey(self, event, hotkey, *args):
        winsound.MessageBeep()
        action = args[0][0][0]

        if action == "adbot":
            AdThread()
            return

        if self.currentthread is not None:
            if self.ocr_temp is not None:
                self.ocr_temp = None
            
            if self.st is not None:
                self.st.stop()
                self.st.join()
                self.st = None

            self.currentthread.stop()
            self.currentthread = None
        elif action == "killaround":
            self.st = ScreenshotThread(CancellationToken())
            self.ocr_temp = OCR(self.st)

            self.currentthread = KillAroundThread(self.ocr_temp, meat_type="scorpionmeat")
        elif action == "orcbot":
            self.currentthread = OrcThread()
        elif action == "holdright":
            rightdown()
        elif action == "clicker":
            self.currentthread = ClickerThread()
        elif action == "alchemy":
            self.currentthread = AlchemyThread(self.alchemypositions)
        elif action == "mpregenbot":
            if self.mpregenbotthread is None:
                self.mpregenbotthread = MpRegenThread(self.currentshield)
            else:
                self.mpregenbotthread.stop()
                self.mpregenbotthread = None        
        elif action == "fakeampbot":
            self.currentthread = FakeAmpThread()
        elif action == "repbot":
            if self.repthread is None:
                self.repthread = RepBotThread()
            else:
                self.repthread.stop()
                self.repthread = None
        elif action == "farmbot":            
            if self.farmthread is None:
                self.farmthread = FarmThread(False)
            else:
                self.farmthread.stop()
                self.farmthread = None
        elif action == "farmbot_farm":
            if self.farmthread is None:
                self.farmthread = FarmThread(True)
            else:
                self.farmthread.stop()
                self.farmthread = None
        elif action == "levellingbot":
            self.currentthread = LevellingBotThread(False, "snakemeat")
        elif action == "levellingbot_pit":
            self.currentthread = LevellingBotThread(True, "snakemeat")
        elif action == "logcursor":
            print(position())

        elif "cast_" in action:
            spell = action.replace("cast_", "")
            CastSpellThread(spell)

        elif action == "equipshield":
            EquipItemThread(self.currentshield)

        elif "alchemy_" in action:
            index = int(action.replace("alchemy_", ""))
            self.alchemypositions[index] = position()
        elif action == "resetpositions":
            self.alchemypositions = [None] * 7
        
    def registerhotkeys(self):
        hk = SystemHotkey(consumer=self.handlehotkey)
        hk.register(("control", "shift", "l"), "killaround")
        hk.register(("control", "shift", "i"), "orcbot")
        hk.register(("control", "shift", "u"), "holdright")
        hk.register(("control", "shift", "t"), "clicker")
        hk.register(("control", "shift", "y"), "alchemy")
        hk.register(("control", "shift", "m"), "mpregenbot")
        hk.register(("control", "shift", "k"), "levellingbot")
        hk.register(("control", "shift", "j"), "levellingbot_pit")
        # hk.register(("control", "alt", "shift", "y"), "adbot")
        # hk.register(("control", "alt", "shift", "t"), "fakeampbot")
        hk.register(("control", "alt", "shift", "r"), "repbot")
        hk.register(("control", "alt", "shift", "x"), "farmbot")
        hk.register(("control", "alt", "shift", "c"), "farmbot_farm")
        hk.register(("control", "alt", "shift", "q"), "logcursor")
        # =======
        hk.register(("alt", "1"), "cast_invisibility")
        hk.register(("alt", "2"), "cast_amp")
        hk.register(("alt", "3"), "cast_paralyze")
        hk.register(("alt", "4"), "cast_haste")

        hk.register(("alt", "w"), "cast_blizzard")
        hk.register(("alt", "e"), "cast_earthshockwave")
        hk.register(("alt", "r"), "cast_defenseshield")

        hk.register(("alt", "q"), "cast_greatheal")
        hk.register(("alt", "s"), "cast_greatstaminarecovery")

        hk.register(("control", "b"), "cast_berserk")
        # hk.register(("control", "v"), "cast_pfm")
        # =======
        hk.register(("control", "space"), "equipshield")
        # =======
        hk.register(("control", "kp_1"), "alchemy_0")
        hk.register(("control", "kp_2"), "alchemy_1")
        hk.register(("control", "kp_3"), "alchemy_2")
        hk.register(("control", "kp_4"), "alchemy_3")
        hk.register(("control", "kp_5"), "alchemy_4")
        hk.register(("control", "kp_6"), "alchemy_5")
        hk.register(("control", "kp_7"), "alchemy_6")
        hk.register(("control", "kp_8"), "resetpositions")
        
