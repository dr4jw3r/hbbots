import tkinter as tk
from hotkeyhandler import HotkeyHandler
from pfmwatcher import PfmWatcherThread

# Labels
LABELS = [
    ("CTRL + SHIFT + L", "Kill Around"),
    ("CTRL + SHIFT + I", "Orc Archery Bot"),
    ("CTRL + SHIFT + U", "Toggle Right Button"),
    ("CTRL + SHIFT + Y", "Alchemy Bot"),
    ("CTRL + ALT + SHIFT + Y", "Advert Bot"),
    ("CTRL + ALT + SHIFT + T", "Fake AMP Bot")
]

# Methods
def buildui():
    PADDING_X = 10
    PADDING_Y = 5
    root = tk.Tk()    

    for row, label in enumerate(LABELS):
        tk.Label(root, text=label[0]).grid(row=row, column=1, ipadx=PADDING_X, ipady=PADDING_Y)
        tk.Label(root, text=label[1]).grid(row=row, column=3, ipadx=PADDING_X, ipady=PADDING_Y)

    root.mainloop()

# Start
hkhandler = HotkeyHandler()
hkhandler.registerhotkeys()
buildui()