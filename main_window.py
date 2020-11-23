from tkinter import *
import utils

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Charmander v0.1")
        self.iconbitmap("./etc/charmander.ico")
        self.minsize(320, 0)
        self.config(
            padx=2,
            pady=2
        )
        self.build_ui()

    def build_ui(self):
        self.notif_strvar = StringVar()
        notif_bar = Label(self, anchor=W, textvariable=self.notif_strvar)
        notif_bar.config(
            borderwidth=1,
            relief=RIDGE,
            padx=5,
            pady=5
        )
        notif_bar.pack(side=BOTTOM, fill=X)
        self.set_notif("OK")

    def set_notif(self, notif):
        try:
            self.notif_strvar.set(notif)
        except Exception as e:
            utils.log(e)




