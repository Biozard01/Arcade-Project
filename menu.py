#!/usr/bin/python3

from tkinter import (
    Tk,
    Button,
    Toplevel,
    Label,
    StringVar,
    DoubleVar,
    FLAT,
    Scale,
    Frame,
    RIGHT,
    LEFT,
    BOTH,
    END,
    Scrollbar,
    Listbox,
    Y,
)

from tkinter.font import Font

from button import windowPos, retour, scale, scale_0

from snake import App, size

from morpion import Board


def setup():
    st = Tk()
    windowPos(st, "Menu Principal")

    option = Button(
        st, text="Options", bd=5, font=10, height=2, width=10, command=Option
    )
    credit = Button(
        st,
        text="Crédits & règles des jeux",
        bd=5,
        font=30,
        height=3,
        width=25,
        command=Credit,
    )
    snake = Button(st, text="Snake", bd=5, font=10, height=10, width=20, command=Snake)

    morpion = Button(
        st, text="Morpion", bd=5, font=10, heigh=10, width=20, command=Morpion
    )

    option.place(x=490, y=650)
    credit.place(x=420, y=730)
    snake.place(x=200, y=200)
    morpion.place(x=700, y=200)


def Option():
    op = Toplevel()
    windowPos(op, "Options")
    retour(op)
    scale(op)
    scale_0(op)


def Credit():
    cd = Toplevel()
    windowPos(cd, "Crédits & règles des jeux")
    retour(cd)

    txt1 = (
        "RÈGLES DES JEUX :"
        + "\n But du jeu (snake): Manger le plus de rond rouge sans s'auto-percuter."
        + "\n Objectif : Faire le meilleur score en ne mourant pas."
        + "\n Commandes : touche du clavier (les flèches)."
    )

    txt2 = (
        "\n But du jeu (morpion): Aligner 3 croix, verticalement, horizontalement, diagonalement. PS : laisser jouer l'IA."
        + "\n Objectif : Ne pas perdre face à l'IA et marquer le plus de point."
        + "\n Commandes : souris (clique gauche)."
    )

    txt3 = "\n CRÉDITS :" + "\n Arthur Laforest" + "\n Cyrian Philippot"

    txt4 = "\n Programmation :" + "\n Arthur Laforest" + "\n Cyrian Philippot"

    txt5 = "\n Design :" + "\n Arthur Laforest" + "\n Cyrian Philippot"

    txt6 = "\n Test :" + "\n Arthur Laforest" + "\n Cyrian Philippot"

    txt7 = "\n Snake :" + "\n Arthur Laforest" + "\n Cyrian Philippot"

    txt8 = "\n Morpion" + "\n Arthur Laforest" + "\n Cyrian Philippot"

    crecre01 = Label(cd, text=txt1, font=10, bg="#6D071A", fg="white")
    crecre01.place(x=250, y=150)

    crecre02 = Label(cd, text=txt2, font=10, bg="#6D071A", fg="white")
    crecre02.place(x=100, y=250)

    crecre03 = Label(cd, text=txt3, font=10, bg="#6D071A", fg="white")
    crecre03.place(x=150, y=350)

    crecre04 = Label(cd, text=txt4, font=10, bg="#6D071A", fg="white")
    crecre04.place(x=650, y=350)

    crecre05 = Label(cd, text=txt5, font=10, bg="#6D071A", fg="white")
    crecre05.place(x=150, y=450)

    crecre06 = Label(cd, text=txt6, font=10, bg="#6D071A", fg="white")
    crecre06.place(x=650, y=450)

    crecre07 = Label(cd, text=txt7, font=10, bg="#6D071A", fg="white")
    crecre07.place(x=150, y=550)

    crecre08 = Label(cd, text=txt8, font=10, bg="#6D071A", fg="white")
    crecre08.place(x=650, y=550)

    fly = cd
    scrollbar = Scrollbar(fly)
    scrollbar.pack(side=LEFT, fill=Y)


def Snake():
    sn = Toplevel()
    windowPos(sn, "Snake")
    retour(sn)
    game = App(sn)
    game.place(x=200, y=100)
    sn.bind("<Key>", game.redirect)

    buttons = Frame(sn, width=35, height=3 * size / 5)
    Button(buttons, text="Start", bd=5, font=3, width=6, command=game.start).grid()
    Button(buttons, text="Stop", bd=5, font=3, width=6, command=game.clean).grid()
    buttons.place(x=100, y=300)

    scoreboard = Frame(sn, width=35, height=2 * size / 5)
    Label(scoreboard, text="Score :").grid()
    Label(scoreboard, textvariable=game.score.counter).grid()

    Label(scoreboard, text="High Score :").grid()
    Label(scoreboard, textvariable=game.score.maximum).grid()
    scoreboard.place(x=100, y=400)


def Morpion():
    mp = Toplevel()
    windowPos(mp, "Morpion")
    retour(mp)

    class GUI:
        def __init__(self):
            self.app = mp
            self.board = Board()
            self.font = Font(family="Helvetica", size=32)
            self.buttons = {}
            for x, y in self.board.fields:
                handler = lambda x=x, y=y: self.move(x, y)
                button = Button(
                    self.app, command=handler, font=self.font, width=2, height=1
                )
                button.grid(ipadx=60, ipady=60, row=y, column=x)

                self.buttons[x, y] = button
            handler = lambda: self.reset()
            button = Button(
                self.app, text="Recommencer", command=handler, bd=5, font=3, width=15
            )
            button.place(x=730, y=10)
            self.update()

        def reset(self):
            self.board = Board()
            self.update()

        def move(self, x, y):
            self.app.config(cursor="watch")
            self.app.update()
            self.board = self.board.move(x, y)
            self.update()
            move = self.board.best()
            if move:
                self.board = self.board.move(*move)
                self.update()
            self.app.config(cursor="")

        def update(self):
            for (x, y) in self.board.fields:
                text = self.board.fields[x, y]
                self.buttons[x, y]["text"] = text
                self.buttons[x, y]["disabledforeground"] = "black"
                if text == self.board.empty:
                    self.buttons[x, y]["state"] = "normal"
                else:
                    self.buttons[x, y]["state"] = "disabled"
            winning = self.board.won()
            if winning:
                lose = Label(
                    mp, text="Perdu !", font=20, width=6, bd=5, bg="#6D071A", fg="white"
                )
                lose.place(x=750, y=300)
                for x, y in winning:
                    self.buttons[x, y]["disabledforeground"] = "red"
                for x, y in self.buttons:
                    self.buttons[x, y]["state"] = "disabled"
                lose.after(10000, lambda: lose.destroy())
            for (x, y) in self.board.fields:
                self.buttons[x, y].update()

    GUI()
