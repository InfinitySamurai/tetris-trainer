import pygame as pg
from enum import Enum, auto

class Inputs(Enum):
    EXIT = auto()
    RESTART = auto()
    HOLD = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    ROTATE_CW = auto()
    ROTATE_CCW = auto()

key_to_action_map = {
    pg.K_ESCAPE: Inputs.EXIT,
    pg.K_r: Inputs.RESTART,
    pg.K_c: Inputs.HOLD,
    pg.K_LSHIFT: Inputs.HOLD,
    pg.K_LEFT: Inputs.MOVE_LEFT,
    pg.K_RIGHT: Inputs.MOVE_RIGHT,
    pg.K_x: Inputs.ROTATE_CW,
    pg.K_z: Inputs.ROTATE_CCW
}

class InputController():
    def __init__(self):
        # disable key repeats
        pg.key.set_repeat()

        self.action_map = {
            Inputs.EXIT: False,
            Inputs.RESTART: False,
            Inputs.HOLD: False,
            Inputs.MOVE_LEFT: False,
            Inputs.MOVE_RIGHT: False,
            Inputs.ROTATE_CW: False,
            Inputs.ROTATE_CCW: False
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
