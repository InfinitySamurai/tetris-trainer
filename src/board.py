import pygame as pg
import numpy as np

from data.settings import colours
from data.tetronimoData import tetronimo_colours, Tetronimoes

class Board:

    def __init__(self, gameSettings):
        self.width = 10
        self.height = 20
        self.preview_col_count = 4
        self.preview_row_count = 3

        self.settings = gameSettings

        self.board_state = np.zeros([gameSettings["num_rows"], gameSettings["num_cols"]], int)
        self.preview_grid = np.zeros([self.preview_row_count * gameSettings["preview_count"], self.preview_col_count], int)

        self.board_state[0][0] = 3
        self.board_state[1][1] = 1
        self.board_state[2][4] = 6

    def draw(self, surface):
        self.draw_static(surface)
        self.draw_board_state(surface)

    def draw_board_state(self, surface):
        num_cols = self.settings["num_cols"]
        num_rows = self.settings["num_rows"]
        cell_size = self.settings["cell_size"]

        for i in range(num_cols):
            for j in range(num_rows):
                cell_state = self.board_state[j, i]

                if cell_state == 0:
                    continue

                colour = tetronimo_colours[Tetronimoes(cell_state)]
                start_position = (self.settings["board_x_pos"] + i * (self.settings["cell_size"] + self.settings["grid_thickness"]), self.settings["board_y_pos"] + j * (self.settings["cell_size"] + self.settings["grid_thickness"]))

                pg.draw.rect(
                    surface,
                    colour,
                    (
                        start_position,
                        (cell_size, cell_size)
                    ),
                )

    
    def draw_static(self, surface):
        board_x_pos = self.settings["board_x_pos"]
        board_y_pos = self.settings["board_y_pos"]
        cell_size = self.settings["cell_size"]
        grid_thickness = self.settings["grid_thickness"]
        num_cols = self.settings["num_cols"]

        # Main game area
        draw_grid(surface, board_x_pos, board_y_pos, num_cols, self.settings["num_rows"], cell_size,  grid_thickness )
        grid_width = (cell_size + grid_thickness) * num_cols

        # preview grid
        preview_x = board_x_pos + grid_width + self.settings["preview_gap_from_main_grid"]
        draw_grid(surface, preview_x, board_y_pos, self.preview_col_count, self.preview_row_count * self.settings["preview_count"], cell_size, grid_thickness)


def draw_grid(surface, posx: float, posy: float, num_cols: int, num_rows: int, cell_size: float, line_width: int):
    cell_separation = cell_size + line_width
    grid_colour = colours["grid"]

    for i in range(num_cols + 1):
        start_x = posx + i * cell_separation
        start_pos = (start_x, posy)
        end_pos = (start_x, posy + cell_separation * num_rows)
        pg.draw.line(surface, grid_colour, start_pos, end_pos, line_width)

    for j in range(num_rows + 1):
        start_y = posy + j * cell_separation
        start_pos = (posx, start_y)
        end_pos = (posx + num_cols * cell_separation, start_y)
        pg.draw.line(surface, grid_colour, start_pos, end_pos, line_width)