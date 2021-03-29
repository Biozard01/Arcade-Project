#!/usr/bin/python3

from tkinter import Tk, Button, IntVar, Label, Scale


def windowPos(window, name):
    window.title(f"{name}")
    window.overrideredirect(True)
    window.attributes("-topmost", True)
    window.configure(bg="#6D071A")
    window.resizable(False, False)
    FullScreen(window)
    center(window)
    exitt(window)


class FullScreen(object):
    def __init__(self, master):
        self.master = master
        master.geometry(f"{1100}x{900}")


def center(center):
    windowWidth = center.winfo_reqwidth()
    windowHeight = center.winfo_reqheight()

    positionRight = int(center.winfo_screenwidth() / 8 - windowWidth / 3)
    positionDown = int(center.winfo_screenheight() / 8 - windowHeight / 3)

    center.geometry(f"+{positionRight}+{positionDown}")


def retour(current):
    retour = Button(
        current, text="Retour", bd=5, font=3, width=6, command=current.destroy
    )
    retour.place(x=1020, y=60)


def exitt(menu):
    exitt = Button(menu, text="Quitter", bd=5, font=10, width=6, command=menu.quit)
    exitt.place(x=1020, y=10)


def scale(windows):
    ma_valeur = IntVar()
    barre = Scale(
        windows,
        orient="horizontal",
        from_=0,
        to=5,
        resolution=0.5,
        tickinterval=1,
        length=350,
        bd=4,
        var=ma_valeur,
    )
    barre.place(x=375, y=750)

    son = Label(windows, text="Volume", bd=3, font=10)
    son.place(x=525, y=720)

    ma_valeur_barre = IntVar(value=None)
    ma_valeur_barre.set(0)

    affichage = Label(windows, textvariable=ma_valeur_barre, width=50)
    affichage.place(x=375, y=750)


def scale_0(windows):
    ma_valeur = IntVar()
    barre = Scale(
        windows,
        orient="horizontal",
        from_=0,
        to=5,
        resolution=1,
        tickinterval=1,
        length=350,
        bd=4,
        var=ma_valeur,
    )
    barre.place(x=375, y=550)

    luminosite = Label(windows, text="Luminosité", bd=3, font=10)
    luminosite.place(x=510, y=520)

    ma_valeur_barre = IntVar(value=None)
    ma_valeur_barre.set(0)

    affichage = Label(windows, textvariable=ma_valeur_barre, width=50)
    affichage.place(x=375, y=550)

