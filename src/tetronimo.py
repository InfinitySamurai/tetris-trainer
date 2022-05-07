from typing import Tuple

from data.tetronimoData import Tetronimoes, tetronimo_shapes, tetronimo_colours
from drawUtils import draw_sqaure_at_grid


class Tetronimo():
    def __init__(self, piece_type: Tetronimoes, position: Tuple[int, int], board_pos: Tuple[int, int], cell_size, grid_thickness):
        self.piece = piece_type
        self.piece_data = tetronimo_shapes[piece_type]
        self.position = position
        self.board_pos = board_pos
        self.cell_size = cell_size
        self.grid_thickness = grid_thickness

    def draw(self, surface):
        for i in range(self.piece_data.shape[0]):
            for j in range(self.piece_data.shape[1]):
                cell_state = self.piece_data[j, i]

                if cell_state == 0:
                    continue

                colour = tetronimo_colours[Tetronimoes(cell_state)]

                draw_sqaure_at_grid(surface, (i, j), (self.board_pos[0], self.board_pos[1]), colour, self.cell_size, self.grid_thickness)