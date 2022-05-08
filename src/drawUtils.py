import pygame as pg
from typing import Tuple

from data.settings import colours


def draw_square_at_grid(surface: pg.Surface, board_pos: Tuple[int, int], cell_pos: Tuple[int, int], colour, settings):
    start_position = cell_to_world_coords(board_pos, cell_pos, settings)
    square = pg.Rect(start_position, (settings["cell_size"], settings["cell_size"]))

    shape_surface = pg.Surface(square.size, pg.SRCALPHA)

    pg.draw.rect(
        shape_surface,
        pg.Color(colour),
        shape_surface.get_rect()
    )

    surface.blit(shape_surface, square)

def draw_grid(surface, posx: float, posy: float, num_rows: int, num_cols: int, grid_colour, settings):
    cell_separation = settings["cell_size"] + settings["grid_thickness"]

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

def cell_to_world_coords(board_coords: Tuple[int, int], cell: Tuple[int, int], settings, offset=(0,0)):
    x = board_coords[0] + cell[1] * (settings["cell_size"] + settings["grid_thickness"]) + settings["grid_thickness"] + offset[0]
    y = board_coords[1] + cell[0] * (settings["cell_size"] + settings["grid_thickness"]) + settings["grid_thickness"] + offset[1]

    return (x, y)