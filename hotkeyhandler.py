import threading
import winsound

from time import sleep
from system_hotkey import SystemHotkey
from inputcontrol import rightdown, rightup

from killaround import KillAroundThread
from castspell import CastSpellThread
from equipitem import EquipItemThread
from alchbot import AlchemyThread

class HotkeyHandler():
    def __init__(self):
        self.currentthread = None

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
            self.currentthread = AlchemyThread()

        elif "cast_" in action:
            spell = action.replace("cast_", "")
            CastSpellThread(spell)

        elif action == "equipshield":
            EquipItemThread("lagishield")

    def registerhotkeys(self):
        hk = SystemHotkey(consumer=self.handlehotkey)
        hk.register(("control", "shift", "l"), "killaround")
        hk.register(("control", "shift", "u"), "holdright")
        hk.register(("control", "shift", "y"), "alchemy")
        # =======
        hk.register(("alt", "1"), "cast_invisibility")
        hk.register(("alt", "2"), "cast_amp")
        hk.register(("alt", "3"), "cast_paralyze")

        hk.register(("alt", "w"), "cast_icestrike")
        hk.register(("alt", "e"), "cast_energystrike")

        hk.register(("alt", "q"), "cast_greatheal")
        hk.register(("alt", "s"), "cast_greatstaminarecovery")
        hk.register(("control", "b"), "cast_berserk")
        # =======
        hk.register(("control", "space"), "equipshield")
        
