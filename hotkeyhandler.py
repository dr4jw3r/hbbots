import threading
import winsound

from time import sleep
from system_hotkey import SystemHotkey
from inputcontrol import rightdown, rightup, position

from killaround import KillAroundThread
from castspell import CastSpellThread
from equipitem import EquipItemThread
from alchbot import AlchemyThread

class HotkeyHandler():
    def __init__(self):
        self.currentthread = None
        self.alchemypositions = [None] * 7

    def handlehotkey(self, event, hotkey, *args):
        winsound.MessageBeep()
        action = args[0][0][0]

        if self.currentthread is not None:
            self.currentthread.stop()
            self.currentthread = None
        elif action == "killaround":
            self.currentthread = KillAroundThread()
        elif action == "holdright":
            rightdown()
        elif action == "alchemy":
            self.currentthread = AlchemyThread(self.alchemypositions)

        elif "cast_" in action:
            spell = action.replace("cast_", "")
            CastSpellThread(spell)

        elif action == "equipshield":
            EquipItemThread("lagishield")

        elif "alchemy_" in action:
            index = int(action.replace("alchemy_", ""))
            self.alchemypositions[index] = position()
        elif action == "resetpositions":
            self.alchemypositions = [None] * 7
        
    def registerhotkeys(self):
        hk = SystemHotkey(consumer=self.handlehotkey)
        hk.register(("control", "shift", "l"), "killaround")
        hk.register(("control", "shift", "u"), "holdright")
        hk.register(("control", "shift", "y"), "alchemy")
        # =======
        hk.register(("alt", "1"), "cast_invisibility")
        hk.register(("alt", "2"), "cast_amp")
        hk.register(("alt", "3"), "cast_paralyze")
        hk.register(("alt", "4"), "cast_haste")

        hk.register(("alt", "w"), "cast_blizzard")
        hk.register(("alt", "e"), "cast_earthshockwave")

        hk.register(("alt", "q"), "cast_greatheal")
        hk.register(("alt", "s"), "cast_greatstaminarecovery")
        hk.register(("control", "b"), "cast_berserk")
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
        
