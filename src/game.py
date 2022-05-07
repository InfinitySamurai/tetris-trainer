import pygame as pg

from board import Board
from input import Inputs

class Game:
    def __init__(self, game_settings):
        self.game_settings = game_settings
        self.board = Board(game_settings)
        self.gravity = game_settings["start_gravity"]

    def draw(self, surface):
        self.board.draw(surface)

    def update(self, input_map, player_settings):
        gravity = self.gravity
        if input_map[Inputs.SOFT_DROP]["held"]:
            gravity = gravity * player_settings["soft_drop_factor"]

        self.board.update(input_map, gravity)