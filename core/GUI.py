import tkinter as tk

class GUI(object):
    def __init__(self):
        self.PADDING_X = 10
        self.PADDING_Y = 5
        self.LABELS = [
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

    def buildui(self):
        root = tk.Tk()
        root.title("HBBOT")

        for row, label in enumerate(self.LABELS):
            tk.Label(root, text=label[0]).grid(
                row=row, column=1, ipadx=self.PADDING_X, ipady=self.PADDING_Y)
            tk.Label(root, text=label[1]).grid(
                row=row, column=3, ipadx=self.PADDING_X, ipady=self.PADDING_Y)

        root.mainloop()
        return 0
