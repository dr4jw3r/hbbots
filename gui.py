import tkinter as tk

from core.hotkeyhandler import HotkeyHandler

# Labels
LABELS = [
    ("CTRL + SHIFT + L", "Kill Around"),
    ("CTRL + SHIFT + I", "Orc Archery Bot"),
    ("CTRL + SHIFT + U", "Toggle Right Button"),
    ("CTRL + SHIFT + Y", "Alchemy Bot"),
    ("CTRL + SHIFT + K", "Levelling Bot"),
    ("CTRL + SHIFT + J", "Levelling Bot - Start at pit"),
    ("CTRL + ALT + SHIFT + Y", "Advert Bot"),
    ("CTRL + ALT + SHIFT + T", "Fake AMP Bot"),
    ("CTRL + ALT + SHIFT + R", "Rep Bot"),
    ("CTRL + ALT + SHIFT + X", "Farm Bot"),
    ("CTRL + ALT + SHIFT + C", "Farm Bot - Start at farm"),
]

# Methods
def buildui():
    PADDING_X = 10
    PADDING_Y = 5
    root = tk.Tk()    
    root.title("HBBOT")

    for row, label in enumerate(LABELS):
        tk.Label(root, text=label[0]).grid(row=row, column=1, ipadx=PADDING_X, ipady=PADDING_Y)
        tk.Label(root, text=label[1]).grid(row=row, column=3, ipadx=PADDING_X, ipady=PADDING_Y)

    root.mainloop()

# Start
hkhandler = HotkeyHandler()
hkhandler.registerhotkeys()
buildui()