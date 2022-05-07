import pygame as pg
from typing import Tuple

from data.settings import colours


def draw_sqaure_at_grid(surface, cell_pos: Tuple[int, int], board_pos: Tuple[float, float], colour, cell_size, grid_thickness):
    start_x = board_pos[0] + cell_pos[0] * (cell_size + grid_thickness) + grid_thickness
    start_y = board_pos[1] + cell_pos[1] * (cell_size + grid_thickness) + grid_thickness
    start_position = (start_x, start_y)

    pg.draw.rect(
        surface,
        colour,
        (
            start_position,
            (cell_size, cell_size)
        ),
    )

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