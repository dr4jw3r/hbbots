from ctypes import *
from threading import Thread
from inputcontrol import *
from imagesearch import imagesearch_numLoop
from pyautogui import position

class CastSpellThread(object):
    def __init__(self, spellname):
        self.CLICKOFFSET = 5
        self.SPELLS = [
            { 'name': 'defenseshield', 'circle': 2 },
            { 'name': 'greatheal', 'circle': 3 },
            { 'name': 'greatstaminarecovery', 'circle': 3 },
            { 'name': 'invisibility', 'circle': 4 },
            { 'name': 'paralyze', 'circle': 4 },
            { 'name': 'pfm', 'circle': 4 },
            { 'name': 'tripleenergybolt', 'circle': 5 },
            { 'name': 'icestrike', 'circle': 6 },
            { 'name': 'berserk', 'circle': 6 },
            { 'name': 'haste', 'circle': 6 },
            { 'name': 'amp', 'circle': 7 },
            { 'name': 'energystrike', 'circle': 7 },
            { 'name': 'blizzard', 'circle': 0 },
            { 'name': 'earthshockwave', 'circle': 0 },
        ]

        thread = Thread(target=self.run, args=(), kwargs={'spellname': spellname})
        thread.daemon = True
        thread.start()
    
    def findspell(self, spellname):
        for spell in self.SPELLS:
            if spell['name'] == spellname:
                return spell

    def opencircle(self, spell):
        keydown("ctrlleft")
        keypress(str(spell['circle']))
        keyup("ctrlleft")

    def run(self, spellname):
        imagepath = "./common/samples/spells/" + spellname + ".png"

        spell = self.findspell(spellname)
        self.opencircle(spell)
        pos = imagesearch_numLoop(imagepath, 0.1, 4)
        print(pos)
        cursorpos = position()
        inputdisable()
        moveto(pos, self.CLICKOFFSET)
        click()
        moveto(cursorpos)
        keyup("altleft")
        inputenable()

    def stop(self):
        pass