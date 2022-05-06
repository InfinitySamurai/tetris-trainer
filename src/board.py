import pygame as pg
from data.settings import colours

class Board:

    def __init__(self, gameSettings):
        self.width = 10
        self.height = 20
        self.preview_col_count = 4
        self.preview_row_count = 3

        self.settings = gameSettings

    def draw(self, surface):
        self.draw_static(surface)

    def draw_static(self, surface):
        # Main game area
        draw_grid(surface, self.settings["board_x_pos"], self.settings["board_y_pos"], self.settings["num_cols"], self.settings["num_rows"], self.settings["cell_size"],  self.settings["grid_thickness"] )

        # preview grid
        preview_x = self.settings["board_x_pos"] + self.settings["board_width"] + self.settings["preview_gap_from_main_grid"]
        draw_grid(surface, preview_x, self.settings["board_y_pos"], self.preview_col_count, self.preview_row_count * self.settings["preview_count"], self.settings["cell_size"], self.settings["grid_thickness"])


def draw_grid(surface, posx: float, posy:float, num_cols: int, num_rows: int, cell_size: float, line_width: int):
    cell_separation = cell_size + line_width
    for i in range(num_cols + 1):
        start_x = posx + i * cell_separation
        start_pos = (start_x, posy)
        end_pos = (start_x, posy + cell_separation * num_rows)
        pg.draw.line(surface, colours["grid"], start_pos, end_pos, line_width)
    for j in range(num_rows + 1):
        start_y = posy + j * cell_separation
        start_pos = (posx, start_y)
        end_pos = (posx + num_cols * cell_separation, start_y)
        pg.draw.line(surface, colours["grid"], start_pos, end_pos, line_width)