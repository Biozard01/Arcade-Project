#!/usr/bin/python3
import json
from operator import itemgetter


def save(highscores):
    with open("data.json", "w") as file:
        json.dump(highscores, file)  # Write the list to the json file.


def load():
    try:
        with open("data.json", "r") as file:
            highscores = json.load(file)  # Read the json file.
    except FileNotFoundError:
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump([[0]], file)
    # Sorted by the score.
    return max(sorted(highscores, key=itemgetter(0), reverse=True)[0])

