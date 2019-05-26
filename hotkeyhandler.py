import threading
import winsound

from time import sleep
from system_hotkey import SystemHotkey
from inputcontrol import rightdown, rightup

from killaround import KillAroundThread
from castspell import CastSpellThread
from equipitem import EquipItemThread

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

        elif action == "castenergybolt":
            CastSpellThread("energybolt")
        elif action == "castinvisibility":
            CastSpellThread("invisibility")
        elif action == "castgreatheal":
            CastSpellThread("greatheal")
        elif action == "castgreatstaminarecovery":
            CastSpellThread("greatstaminarecovery")
        elif action == "casttripleenergybolt":
            CastSpellThread("tripleenergybolt")

        elif action == "equipshield":
            print("uah")
            EquipItemThread("scutumshield")

    def registerhotkeys(self):
        hk = SystemHotkey(consumer=self.handlehotkey)
        hk.register(("control", "shift", "l"), "killaround")
        hk.register(("control", "shift", "u"), "holdright")
        # =======
        hk.register(("alt", "1"), "castinvisibility")
        hk.register(("alt", "3"), "casttripleenergybolt")
        hk.register(("alt", "q"), "castgreatheal")
        hk.register(("alt", "s"), "castgreatstaminarecovery")
        # =======
        hk.register(("control", "space"), "equipshield")
        
