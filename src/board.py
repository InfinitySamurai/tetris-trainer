import random
import numpy as np

from data.settings import colours
from data.tetronimoData import tetronimo_colours, Tetronimoes
from drawUtils import draw_grid, draw_sqaure_at_grid
from input import Inputs
from tetronimo import Tetronimo

class Board:
    def __init__(self, game_settings):
        self.width = 10
        self.height = 20
        self.preview_col_count = 4
        self.preview_row_count = 3

        self.settings = game_settings

        self.board_state = np.zeros([game_settings["num_rows"], game_settings["num_cols"]], int)
        self.preview_grid = np.zeros([self.preview_row_count * game_settings["preview_count"], self.preview_col_count], int)

        self.current_tetronimo = Tetronimo(self, random.choice(list(Tetronimoes)), (0, 0), self.settings)

    def lock_piece(self):
        tetronimo = self.current_tetronimo
        for tetronimo_row in range(tetronimo.piece_data.shape[0]):
            for tetronimo_col in range(tetronimo.piece_data.shape[1]):
                cell_state = tetronimo.piece_data[tetronimo_row, tetronimo_col]

                if cell_state == 0:
                    continue 
                
                board_row = tetronimo.position[0] + tetronimo_row
                board_col = tetronimo.position[1] + tetronimo_col 

                self.board_state[board_row][board_col] = tetronimo.piece.value

        self.current_tetronimo = Tetronimo(self, random.choice(list(Tetronimoes)), (0, 0), self.settings)

    def update(self, input_map, gravity, player_settings):
        if input_map[Inputs.MOVE_RIGHT]["frames"] == 1:
            self.current_tetronimo.try_move(1)
        if input_map[Inputs.MOVE_RIGHT]["das_active"] and input_map[Inputs.MOVE_RIGHT]["frames"] % player_settings["automatic_repeat_rate"] == 0:
            self.current_tetronimo.try_move(1)
        if input_map[Inputs.MOVE_LEFT]["frames"] == 1:
            self.current_tetronimo.try_move(-1)
        if  input_map[Inputs.MOVE_LEFT]["das_active"] and input_map[Inputs.MOVE_LEFT]["frames"] % player_settings["automatic_repeat_rate"] == 0:
            self.current_tetronimo.try_move(-1)
        if input_map[Inputs.ROTATE_CW]["frames"] == 1:
            self.current_tetronimo.try_rotate(3)
        if input_map[Inputs.ROTATE_CCW]["frames"] == 1:
            self.current_tetronimo.try_rotate(1)
        if input_map[Inputs.ROTATE_180]["frames"] == 1:
            self.current_tetronimo.try_rotate(2)

        if input_map[Inputs.HARD_DROP]["frames"] == 1:
            while self.current_tetronimo.try_drop():
                continue
            self.lock_piece()

        if self.current_tetronimo.ready_to_lock(self.settings["lock_ticks"]):
            self.lock_piece()

        self.current_tetronimo.update(gravity)

    def draw(self, surface):
        self.draw_static(surface)
        self.draw_board_state(surface)
        self.current_tetronimo.draw(surface)

    def draw_board_state(self, surface):
        for row in range(self.settings["num_rows"]):
            for col in range(self.settings["num_cols"]):
                cell_state = self.board_state[row][col]

                if cell_state == 0:
                    continue

                colour = tetronimo_colours[Tetronimoes(cell_state)]
                draw_sqaure_at_grid(surface, (row, col), colour, self.settings)

    
    def draw_static(self, surface):
        board_x_pos = self.settings["board_x_pos"]
        board_y_pos = self.settings["board_y_pos"]
        cell_size = self.settings["cell_size"]
        grid_thickness = self.settings["grid_thickness"]
        num_cols = self.settings["num_cols"]

        # Main game area
        draw_grid(surface, board_x_pos, board_y_pos, self.settings["num_rows"], self.settings["num_cols"], self.settings )
        grid_width = (cell_size + grid_thickness) * num_cols

        # preview grid
        preview_x = board_x_pos + grid_width + self.settings["preview_gap_from_main_grid"]
        draw_grid(surface, preview_x, board_y_pos, self.preview_row_count * self.settings["preview_count"], self.preview_col_count, self.settings )

