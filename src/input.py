import pygame as pg
from enum import Enum, auto

class Inputs(Enum):
    EXIT = auto()
    HOLD = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()

key_to_action_map = {
    pg.K_ESCAPE: Inputs.EXIT,
    pg.K_c: Inputs.HOLD,
    pg.K_LSHIFT: Inputs.HOLD
}
class InputController():
    def __init__(self):
        # disable key repeats
        pg.key.set_repeat()

        self.action_map = {
            Inputs.EXIT: False,
            Inputs.HOLD: False,
            Inputs.MOVE_LEFT: False,
            Inputs.MOVE_RIGHT: False
        }

    def get_input(self):
        keydown_events = pg.event.get(pg.KEYDOWN)
        keyup_events = pg.event.get(pg.KEYUP)

        for event in keydown_events:
            if event.key in key_to_action_map:
                mapped_action = key_to_action_map[event.key]
                self.action_map[mapped_action] = True
        
        for event in keyup_events:
            if event.key in key_to_action_map:
                mapped_action = key_to_action_map[event.key]
                self.action_map[mapped_action] = False

        return self.action_map
