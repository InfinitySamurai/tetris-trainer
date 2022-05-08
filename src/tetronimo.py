import copy
from typing import Tuple
import numpy as np
import pygame as pg

import data.tetronimoData as tetronimoData
from data.settings import colours
from drawUtils import cell_to_world_coords, draw_grid, draw_square_at_grid

class Tetronimo():
    def __init__(self, piece_type: tetronimoData.Tetronimoes, settings):
        self.piece = piece_type
        self.piece_data = tetronimoData.tetronimo_shapes[piece_type]
        self.position = (0, 0)
        self.settings = settings
        self.ticks_since_last_drop = 0
        self.failed_drop = False
        self.lock_tick_counter = 0
        self.rotations_since_failed_drop = 0
        self.current_rotation: tetronimoData.Rotation = tetronimoData.Rotation.START

    def try_move(self, board, direction):
        next_position = (self.position[0], self.position[1] + direction)
        if not self.check_collision(board, next_position, self.piece_data):
            self.position = next_position
            return True
        return False
    
    # rotations is how many time to rotate counter clockwise because that's how numpy does it
    def try_rotate(self, board, rotations):
        next_piece_data = np.rot90(self.piece_data, rotations)
        next_rotation = tetronimoData.Rotation((self.current_rotation.value + rotations) % tetronimoData.possible_rotation_count)
        next_position = self.position

        if self.check_collision(board, next_position, next_piece_data):
            kick_table = tetronimoData.kick_table_I if self.piece == tetronimoData.Tetronimoes.I else tetronimoData.kick_table
            for kick_data in kick_table[(self.current_rotation.value, next_rotation.value)]:
                new_position_to_check = (next_position[0] - kick_data[1], next_position[1] + kick_data[0])
                if not self.check_collision(board, new_position_to_check, next_piece_data):
                    self.do_rotation(next_piece_data, next_rotation, new_position_to_check)
                    return True
            return False

        self.do_rotation(next_piece_data, next_rotation, self.position)

        return True

    def do_rotation(self, next_piece_data, next_rotation, next_position):
        self.piece_data = next_piece_data
        self.position = next_position
        self.lock_tick_counter = 0
        self.current_rotation = next_rotation

        if self.failed_drop:
            self.rotations_since_failed_drop += 1

    def try_drop(self, board):
        next_position = (self.position[0] + 1, self.position[1])
        if self.check_collision(board, next_position, self.piece_data):
            self.failed_drop = True
            return False

        self.position = next_position
        self.failed_drop = False
        self.lock_tick_counter = 0
        self.rotations_since_failed_drop = 0
        return True

    def check_collision(self, board, position: Tuple[int, int], piece_data):
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

                board_cell_state = board.board_state[board_row][board_col]
                if board_cell_state > 0:
                    return True

        return False

    def ready_to_lock(self, lock_ticks, lock_max_rotations):
        if self.lock_tick_counter > lock_ticks or self.rotations_since_failed_drop > lock_max_rotations:
            return True
        return False

    def update(self, board, gravity):
        self.ticks_since_last_drop += 1
        if self.failed_drop:
            self.lock_tick_counter += 1
        if self.ticks_since_last_drop * gravity >= 1:
            self.ticks_since_last_drop = 0
            self.try_drop(board)
            

    def draw(self, board, surface):
        self.draw_piece(surface, (self.settings["board_x_pos"], self.settings["board_y_pos"]), self.piece_data, self.position)
        self.draw_ghost(board, surface)

    def draw_piece(self, surface, board_pos, piece_data, position, alpha = 255):
        for row in range(piece_data.shape[0]):
            for col in range(piece_data.shape[1]):
                cell_state = piece_data[row][col]

                if cell_state == 0:
                    continue

                colour = tetronimoData.tetronimo_colours[tetronimoData.Tetronimoes(cell_state)]
                colour_with_alpha = (*colour, alpha)

                draw_square_at_grid(surface, board_pos, (position[0] + row, position[1] + col), colour_with_alpha, self.settings)

        if self.settings["debug"]:
            bounding_box_size = (self.settings["cell_size"] + self.settings["grid_thickness"]) * piece_data.shape[0]
            start_pos = cell_to_world_coords((self.settings["board_x_pos"], self.settings["board_y_pos"]), position, self.settings)
            pg.draw.rect(surface, (0, 255, 0), (start_pos, (bounding_box_size, bounding_box_size)), 2)

            draw_grid(surface, start_pos[0], start_pos[1], piece_data.shape[0], piece_data.shape[0], colours["debug_green"], self.settings)

    def draw_ghost(self, board, surface: pg.Surface):
        tetronimo_copy = copy.deepcopy(self)
        while tetronimo_copy.try_drop(board):
            continue

        self.draw_piece(surface, (self.settings["board_x_pos"], self.settings["board_y_pos"]), tetronimo_copy.piece_data, tetronimo_copy.position, 80)
        return