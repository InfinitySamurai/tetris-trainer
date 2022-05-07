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

das_actions = [Inputs.MOVE_LEFT, Inputs.MOVE_RIGHT]

class InputController():
    def __init__(self, player_settings):
        # disable key repeats
        pg.key.set_repeat()
        self.player_settings = player_settings

        self.action_map = {
            Inputs.EXIT: {"held": False, "frames": 0},
            Inputs.RESTART: {"held": False, "frames": 0},
            Inputs.HOLD: {"held": False, "frames": 0},
            Inputs.MOVE_LEFT: {"held": False, "frames": 0, "das": False},
            Inputs.MOVE_RIGHT: {"held": False, "frames": 0, "das": False},
            Inputs.ROTATE_CW: {"held": False, "frames": 0},
            Inputs.ROTATE_CCW: {"held": False, "frames": 0}
        }

    def get_input(self):
        keydown_events = pg.event.get(pg.KEYDOWN)
        keyup_events = pg.event.get(pg.KEYUP)

        for event in keydown_events:
            if event.key in key_to_action_map:
                mapped_action = key_to_action_map[event.key]
                self.action_map[mapped_action]["held"] = True
        
        for event in keyup_events:
            if event.key in key_to_action_map:
                mapped_action = key_to_action_map[event.key]
                self.action_map[mapped_action]["held"] = False
                self.action_map[mapped_action]["frames"] = 0

                if mapped_action in das_actions:
                    self.action_map[mapped_action]["das"] = False

        return self.action_map

    def update(self):
        for key in self.action_map:
            if self.action_map[key]['held']:
                self.action_map[key]['frames'] += 1

                # Figure out if DAS if active
                if key in das_actions:
                    if self.action_map[key]["frames"] > self.player_settings["delayed_auto_shift"]:
                        self.action_map[key]["das"] = True
