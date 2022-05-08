import numpy as np

from drawUtils import draw_grid
from tetronimo import Tetronimo
from data.settings import colours


class Preview:
    def __init__(self, settings):
        self.settings = settings
        self.preview_col_count = 4
        self.preview_row_count = 3

        self.preview_grid = np.zeros(
            [
                self.preview_row_count * settings["preview_count"],
                self.preview_col_count,
            ],
            np.int8,
        )

        return

    def draw(self, surface, pieces: list[Tetronimo]):
        draw_grid(
            surface,
            (self.settings["preview_x_pos"], self.settings["board_y_pos"]),
            self.preview_row_count * self.settings["preview_count"],
            self.preview_col_count,
            colours["grid"],
            self.settings,
        )

        for index, piece in enumerate(pieces):
            piece.draw_piece(
                surface,
                (self.settings["preview_x_pos"], self.settings["board_y_pos"]),
                piece.piece_data,
                (3 * index, 0),
            )
        return
