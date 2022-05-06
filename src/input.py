import pygame as pg
from enum import Enum, auto

class Inputs(Enum):
    EXIT = auto()

key_to_input_map = {
    pg.K_ESCAPE: Inputs.EXIT
}

class InputController():
    def __init__(self):
        # disable key repeats
        pg.key.set_repeat()

        self.input_map = {
            Inputs.EXIT: False
        }

    def get_input(self):
        keydown_events = pg.event.get(pg.KEYDOWN)
        keyup_events = pg.event.get(pg.KEYUP)

        if len(keydown_events) > 0:
            print(keydown_events)
            print(pg.K_ESCAPE)
            print(self.input_map)

        for event in keydown_events:
            if event.key in key_to_input_map:
                mapped_input = key_to_input_map[event.key]
                self.input_map[mapped_input] = True

        return self.input_map
