import pygame as pg

from board import Board

class Game:
    def __init__(self, gameSettings):
        self.gameSettings = gameSettings
        self.board = Board(gameSettings)

    def draw(self, surface):
        self.board.draw(surface)

