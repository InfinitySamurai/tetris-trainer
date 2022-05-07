from typing import Tuple
import numpy as np

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
        if not self.check_collision(next_position, self.piece_data):
            self.position = next_position
    
    def try_rotate(self, direction):
        next_piece_data = np.rot90(self.piece_data)
        if not self.check_collision(self.position, next_piece_data):
            self.piece_data = next_piece_data

    def try_drop(self):
        next_position = (self.position[0] + 1, self.position[1])
        if not self.check_collision(next_position, self.piece_data):
            self.position = next_position

    def check_collision(self, position: Tuple[int, int], piece_data):
        for tetronimo_row in range(piece_data.shape[0]):
            for tetronimo_col in range(piece_data.shape[1]):
                cell_state = piece_data[tetronimo_row, tetronimo_col]

                if cell_state == 0:
                    continue 
                
                board_row = position[0] + tetronimo_row
                board_col = position[1] + tetronimo_col

                if board_row > self.settings["num_rows"] - 1:
                    return True
                if board_col > self.settings["num_cols"] - 1 or board_col < 0:
                    return True

                board_cell_state = self.board.board_state[board_row][board_col]
                if board_cell_state > 0:
                    return True
        return False

    def update(self, gravity):
        self.ticks_since_last_drop += 1
        if self.ticks_since_last_drop * gravity >= 1:
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