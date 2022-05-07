from typing import Tuple

from data.tetronimoData import Tetronimoes, tetronimo_shapes


class Tetronimo():
    def __init__(self, piece_type: Tetronimoes, position: Tuple[int, int], board_pos: Tuple[int, int]):
        self.piece = piece_type
        self.piece_data = tetronimo_shapes[piece_type]
        self.position = position
        self.board_pos = board_pos

    def draw(self, surface):
        
        return