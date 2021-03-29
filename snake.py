#!/usr/bin/python3

from tkinter import Grid, Frame, Canvas, StringVar, Button, Label, Tk

from random import randint, choice

from bddsto import load, itemgetter, save

grad = 70
pixel = 10
STEP = 2 * pixel
size = pixel * grad

apple_size = 0.9
snake_size = 1
apple = pixel * apple_size
snake = pixel * snake_size

background_color = "#6D071A"
apple_color = "red"

color = ["green", "yellow", "blue", "purple", "pink"]

snake_color = choice(color)

SN = "snake"
AP = "apple"
SIZE = {SN: snake, AP: apple}

UP = "Up"
DOWN = "Down"
RIGHT = "Right"
LEFT = "Left"

directions = {UP: [0, -1], DOWN: [0, 1], RIGHT: [1, 0], LEFT: [-1, 0]}
AXES = {UP: "Vertical", DOWN: "Vertical", RIGHT: "Horizontal", LEFT: "Horizontal"}
REFRESH_TIME = 120


class App(Canvas):
    def __init__(self, boss=None):
        super().__init__(boss)
        self.configure(width=size, height=size, bg=background_color)
        self.running = 0
        self.snake = None
        self.apple = None
        self.direction = None
        self.current = None
        self.score = Scores(boss)

    # gère le boutton start
    def start(self):
        if self.running == 0:
            self.snake = Snake(self)
            self.apple = Apple(self)
            self.direction = RIGHT
            self.current = Movement(self, RIGHT)
            self.current.begin()
            self.running = 1

    # gère le boutton stop
    def clean(self):
        global REFRESH_TIME
        if self.running == 1:
            self.score.reset()
            self.current.stop()
            self.running = 0
            self.apple.delete()
            REFRESH_TIME = 120
            for block in self.snake.blocks:
                block.delete()

    def redirect(self, event):
        if (
            1 == self.running
            and event.keysym in AXES.keys()
            and AXES[event.keysym] != AXES[self.direction]
        ):
            self.current.flag = 0
            self.direction = event.keysym
            self.current = Movement(self, event.keysym)
            self.current.begin()


class Scores:
    def __init__(self, boss=None):
        self.counter = StringVar(boss, "0")
        self.highscores = load()
        self.maximum = StringVar(boss, self.highscores)

    def increment(self):
        score = int(self.counter.get()) + 1

        loadScore = self.highscores
        self.counter.set(str(score))
        self.maximum.set(str(loadScore))

        if score > loadScore:
            save([[score]])

    # remet le score à 0
    def reset(self):
        self.counter.set("0")


class Shape:
    def __init__(self, can, a, b, kind):
        self.can = can
        self.x, self.y = a, b
        self.kind = kind
        # si kind (espèce en anglais) et = à snake, donc si kind est init en snake
        if kind == SN:
            self.ref = Canvas.create_rectangle(
                self.can,
                a - snake,
                b - snake,
                a + snake,
                b + snake,
                fill=snake_color,
                width=2,
            )
        # si kind (espèce en anglais) et = à apple, donc si kind est init en apple
        elif kind == AP:
            self.ref = Canvas.create_oval(
                self.can,
                a - apple,
                b - apple,
                a + snake,
                b + snake,
                fill=choice(color),
                width=2,
            )

    # déplacement du corps du snake
    def modify(self, a, b):
        self.x, self.y = a, b
        self.can.coords(
            self.ref,
            a - SIZE[self.kind],
            b - SIZE[self.kind],
            a + SIZE[self.kind],
            b + SIZE[self.kind],
        )

    def delete(self):
        self.can.delete(self.ref)


class Apple(Shape):
    def __init__(self, can):
        self.can = can
        p = int(grad / 2 - 1)
        n, m = randint(0, p), randint(0, p)
        a, b = pixel * (2 * n + 1), pixel * (2 * m + 1)
        # tant que la pomme a les même coordonées que la tête du snake
        while [a, b] in [[block.x, block.y] for block in self.can.snake.blocks]:
            # fait apparaitre la pomme dans un endroit aléatoire
            n, m = randint(0, p), randint(0, p)
            a, b = pixel * (2 * n + 1), pixel * (2 * m + 1)
        super().__init__(can, a, b, AP)


class Block(Shape):
    def __init__(self, can, a, y):
        # kind devient snake
        super().__init__(can, a, y, SN)


class Snake:
    def __init__(self, can):
        self.can = can
        a = pixel + 2 * int(grad / 4) * pixel
        self.blocks = [Block(can, a, a), Block(can, a, a + STEP)]

    def move(self, path):
        global REFRESH_TIME
        a = (self.blocks[-1].x + STEP * path[0]) % size
        b = (self.blocks[-1].y + STEP * path[1]) % size
        # si la tête du snake est sur les même coordonnées que la pomme
        if a == self.can.apple.x and b == self.can.apple.y:
            # augmente le score de 1
            self.can.score.increment()
            if REFRESH_TIME > 1:
                REFRESH_TIME -= 1
            else:
                REFRESH_TIME = 1
            # supprime la pomme
            self.can.apple.delete()
            # ajoute un morceau au snake
            self.blocks.append(Block(self.can, a, b))
            # fait apparaitre une nouvelle pomme
            self.can.apple = Apple(self.can)
        # sinon si les coordonnées de la tête du snake sont égale aux coordonnées d'un morceau du corps du snake
        elif [a, b] in [[block.x, block.y] for block in self.blocks]:
            # vide le canvas = lose
            REFRESH_TIME = 120
            self.can.clean()
        # sinon déplace le corps du snake de 1
        else:
            self.blocks[0].modify(a, b)
            self.blocks = self.blocks[1:] + [self.blocks[0]]


class Movement:
    def __init__(self, can, direction):
        self.flag = 1
        self.can = can
        self.direction = direction

    def begin(self):
        # si le jeu tourne, le snake se déplace dans une direction après un temps d'attente (gère la vitesse)
        if self.flag > 0:
            self.can.snake.move(directions[self.direction])
            self.can.after(REFRESH_TIME, self.begin)

    def stop(self):
        self.flag = 0
