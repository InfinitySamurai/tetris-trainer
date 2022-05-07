from typing import Tuple

from data.tetronimoData import Tetronimoes, tetronimo_shapes, tetronimo_colours
from drawUtils import draw_sqaure_at_grid


class Tetronimo():
    def __init__(self, board, piece_type: Tetronimoes, position: Tuple[int, int], settings):
        self.piece = piece_type
        self.piece_data = tetronimo_shapes[piece_type]
        self.position = position
        self.settings = settings
        self.ticks_since_last_drop = 0
        self.board = board

    def try_move(self, direction):
        next_position = (self.position[0], self.position[1] + direction)
        if not self.check_collision(next_position):
            self.position = next_position

    def try_drop(self):
        next_position = (self.position[0] + 1, self.position[1])
        if not self.check_collision(next_position):
            self.position = next_position

    def check_collision(self, position: Tuple[int, int]):
        for row in range(self.piece_data.shape[0]):
            for col in range(self.piece_data.shape[1]):
                cell_state = self.piece_data[row, col]

                if cell_state == 0:
                    continue 

                board_cell_state = self.board.board_state[position[0] + row, position[1] + col]
                if board_cell_state > 0:
                    return True
        return False
                
                

    def update(self):
        self.ticks_since_last_drop += 1
        if self.ticks_since_last_drop * self.settings['start_gravity'] >= 1:
            self.ticks_since_last_drop = 0
            self.try_drop()
            

    def draw(self, surface):
        for row in range(self.piece_data.shape[0]):
            for col in range(self.piece_data.shape[1]):
                cell_state = self.piece_data[row][col]

                if cell_state == 0:
                    continue

                colour = tetronimo_colours[Tetronimoes(cell_state)]

                draw_sqaure_at_grid(surface, (self.position[0] + row, self.position[1] + col), colour, self.settings)