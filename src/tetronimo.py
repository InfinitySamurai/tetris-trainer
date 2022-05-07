from typing import Tuple

from data.tetronimoData import Tetronimoes, tetronimo_shapes, tetronimo_colours
from drawUtils import draw_sqaure_at_grid


class Tetronimo():
    def __init__(self, piece_type: Tetronimoes, position: Tuple[int, int], settings):
        self.piece = piece_type
        self.piece_data = tetronimo_shapes[piece_type]
        self.position = position
        self.settings = settings
        self.frames_since_last_drop = 0

    def try_drop(self):
        self.position = (self.position[0], self.position[1] + 1)

    def update(self):
        self.frames_since_last_drop += 1
        if self.frames_since_last_drop * self.settings['start_gravity'] >= 1:
            self.frames_since_last_drop = 0
            self.try_drop()
            

    def draw(self, surface):
        for i in range(self.piece_data.shape[0]):
            for j in range(self.piece_data.shape[1]):
                cell_state = self.piece_data[j, i]

                if cell_state == 0:
                    continue

                colour = tetronimo_colours[Tetronimoes(cell_state)]

                draw_sqaure_at_grid(surface, (self.position[0] + i, self.position[1] + j), colour, self.settings)