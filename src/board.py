from typing import Tuple
import pygame as pg
import numpy as np

from data.settings import colours
from data.tetronimoData import tetronimo_colours, Tetronimoes
from drawUtils import draw_grid, draw_sqaure_at_grid
from tetronimo import Tetronimo

class Board:

    def __init__(self, gameSettings):
        self.width = 10
        self.height = 20
        self.preview_col_count = 4
        self.preview_row_count = 3

        self.settings = gameSettings

        self.board_state = np.zeros([gameSettings["num_rows"], gameSettings["num_cols"]], int)
        self.preview_grid = np.zeros([self.preview_row_count * gameSettings["preview_count"], self.preview_col_count], int)

        self.current_piece = Tetronimo(Tetronimoes.I, (3, -2), self.settings)

        self.board_state[0][0] = 3
        self.board_state[1][1] = 1
        self.board_state[2][4] = 6

    def update(self):
        self.current_piece.update()
        return

    def draw(self, surface):
        self.draw_static(surface)
        self.draw_board_state(surface)
        self.current_piece.draw(surface)

    def draw_board_state(self, surface):
        for i in range(self.settings["num_cols"]):
            for j in range(self.settings["num_rows"]):
                cell_state = self.board_state[j, i]

                if cell_state == 0:
                    continue

                colour = tetronimo_colours[Tetronimoes(cell_state)]
                draw_sqaure_at_grid(surface, (i, j), colour, self.settings)

    
    def draw_static(self, surface):
        board_x_pos = self.settings["board_x_pos"]
        board_y_pos = self.settings["board_y_pos"]
        cell_size = self.settings["cell_size"]
        grid_thickness = self.settings["grid_thickness"]
        num_cols = self.settings["num_cols"]

        # Main game area
        draw_grid(surface, self.settings )
        grid_width = (cell_size + grid_thickness) * num_cols

        # preview grid
        preview_x = board_x_pos + grid_width + self.settings["preview_gap_from_main_grid"]
        draw_grid(surface, self.settings)

