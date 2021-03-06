import random
import numpy as np
import pygame as pg
from bagManager import BagManager

from data.settings import colours
from data.tetronimoData import tetronimo_colours, Tetronimoes
from tetronimo import Tetronimo
from drawUtils import cell_to_world_coords, draw_grid, draw_square_at_grid
from input import Inputs
from preview import Preview


class Board:
    def __init__(self, settings):
        self.font = pg.font.SysFont("comic sans", 14)
        self.settings = settings
        self.bagManager = BagManager(settings)
        self.preview = Preview(settings)

        self.board_state = np.zeros(
            settings["board_dimensions"], np.int8
        )

        self.current_tetronimo: Tetronimo = self.bagManager.fetch_piece()
        self.held_tetronimo: Tetronimo | None = None
        self.has_swapped_tetronimo = False

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

        self.clear_complete_lines()
        self.current_tetronimo = self.bagManager.fetch_piece()
        self.has_swapped_tetronimo = False

    def clear_complete_lines(self):
        for row_number, row_data in enumerate(self.board_state):
            if np.count_nonzero(row_data) == self.settings["board_dimensions"][1]:
                self.board_state = np.delete(self.board_state, row_number, 0)
                self.board_state = np.insert(
                    self.board_state, 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0
                )

    def update(self, input_map, gravity, player_settings):
        if input_map[Inputs.MOVE_RIGHT]["frames"] == 1:
            self.current_tetronimo.try_move(self, 1)
        if (
            input_map[Inputs.MOVE_RIGHT]["das_active"]
            and input_map[Inputs.MOVE_RIGHT]["frames"]
            % player_settings["automatic_repeat_rate"]
            == 0
        ):
            self.current_tetronimo.try_move(self, 1)
        if input_map[Inputs.MOVE_LEFT]["frames"] == 1:
            self.current_tetronimo.try_move(self, -1)
        if (
            input_map[Inputs.MOVE_LEFT]["das_active"]
            and input_map[Inputs.MOVE_LEFT]["frames"]
            % player_settings["automatic_repeat_rate"]
            == 0
        ):
            self.current_tetronimo.try_move(self, -1)
        if input_map[Inputs.ROTATE_CW]["frames"] == 1:
            self.current_tetronimo.try_rotate(self, 3)
        if input_map[Inputs.ROTATE_CCW]["frames"] == 1:
            self.current_tetronimo.try_rotate(self, 1)
        if input_map[Inputs.ROTATE_180]["frames"] == 1:
            self.current_tetronimo.try_rotate(self, 2)

        if input_map[Inputs.HARD_DROP]["frames"] == 1:
            while self.current_tetronimo.try_drop(self):
                continue
            self.lock_piece()

        if input_map[Inputs.HOLD]["frames"] == 1:
            if self.has_swapped_tetronimo:
                return

            self.has_swapped_tetronimo = True

            if self.held_tetronimo is None:
                self.held_tetronimo = self.current_tetronimo
                self.current_tetronimo = self.bagManager.fetch_piece()
                return

            temp_tetronimo = self.held_tetronimo
            self.held_tetronimo = self.current_tetronimo
            self.current_tetronimo = Tetronimo(temp_tetronimo.piece, self.settings)

        if self.current_tetronimo.ready_to_lock(
            self.settings["lock_ticks"], self.settings["lock_max_rotations"]
        ):
            self.lock_piece()

        self.current_tetronimo.update(self, gravity)

    def draw(self, surface):
        self.draw_static(surface)
        self.draw_board_state(surface)
        self.draw_held_piece(surface)
        self.current_tetronimo.draw(self, surface)
        self.preview.draw(
            surface, self.bagManager.peek_next_pieces(self.settings["preview_count"])
        )

    def draw_held_piece(self, surface):
        held_bounding_box_start_pos = (
            self.settings["held_piece_position"][0] - self.settings["held_piece_box_offset"],
            self.settings["held_piece_position"][1] - self.settings["held_piece_box_offset"],
        )
        pg.draw.rect(
            surface, (255, 255, 255), (held_bounding_box_start_pos, (200, 200)), 2
        )

        held_tetronimo = self.held_tetronimo
        if held_tetronimo is not None:
            x_offset = self.settings["cell_size"] / 2 if held_tetronimo.piece == Tetronimoes.O else 0
            held_tetronimo.draw_piece(
                surface,
                (self.settings["held_piece_position"][0] + x_offset, self.settings["held_piece_position"][1]),
                held_tetronimo.piece_data,
                (0, 0),
            )

    def draw_board_state(self, surface: pg.Surface):
        rows, columns = self.settings["board_dimensions"]
        for row in range(rows):
            for col in range(columns):
                cell_state = self.board_state[row][col]

                if cell_state == 0:
                    continue

                colour = tetronimo_colours[Tetronimoes(cell_state)]
                draw_square_at_grid(
                    surface,
                    self.settings["board_position"],
                    (row, col),
                    colour,
                    self.settings,
                )

        if self.settings["debug"]:
            rows, columns = self.settings["board_dimensions"]
            for row in range(rows):
                for col in range(columns):
                    cell_state = self.board_state[row][col]
                    arr_text = self.font.render(str(cell_state), False, (255, 255, 255))
                    pos = cell_to_world_coords(
                        self.settings["board_position"],
                        (row, col),
                        self.settings,
                        (3, 3),
                    )
                    surface.blit(arr_text, pos)

    def draw_static(self, surface):
        # Main game area
        draw_grid(
            surface,
            self.settings["board_position"],
            self.settings["board_dimensions"],
            colours["grid"],
            self.settings,
        )
