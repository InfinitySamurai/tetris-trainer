import pygame as pg
from typing import Tuple

from data.settings import colours


def draw_sqaure_at_grid(surface, cell_pos: Tuple[int, int], colour, settings):
    start_x = settings["board_x_pos"] + cell_pos[0] * (settings["cell_size"] + settings["grid_thickness"]) + settings["grid_thickness"]
    start_y = settings["board_y_pos"] + cell_pos[1] * (settings["cell_size"] + settings["grid_thickness"]) + settings["grid_thickness"]
    start_position = (start_x, start_y)

    pg.draw.rect(
        surface,
        colour,
        (
            start_position,
            (settings["cell_size"], settings["cell_size"])
        ),
    )

def draw_grid(surface, posx: float, posy: float, num_rows: int, num_cols: int, settings):
    cell_separation = settings["cell_size"] + settings["grid_thickness"]
    grid_colour = colours["grid"]

    for i in range(num_cols + 1):
        start_x = posx + i * cell_separation
        start_pos = (start_x, posy)
        end_pos = (start_x, posy + cell_separation * num_rows)
        pg.draw.line(surface, grid_colour, start_pos, end_pos, settings["grid_thickness"])

    for j in range(num_rows + 1):
        start_y = posy + j * cell_separation
        start_pos = (posx, start_y)
        end_pos = (posx + num_cols * cell_separation, start_y)
        pg.draw.line(surface, grid_colour, start_pos, end_pos, settings["grid_thickness"])