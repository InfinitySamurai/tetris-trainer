import sys
import os
import time
import copy
import pygame as pg
import numpy as np
import random
from itertools import permutations

from data import kicktables
from data import openerData

openers = openerData.openers

tetris_logo = pg.image.load(os.path.join("assets", "tetris.png"))

guide_on = True

board_width = 300
board_height = 700
num_cols = 10
num_rows = 22
screen_width = 1000
screen_height = 800
board_x_pos = screen_width / 2 - board_width / 2
board_y_pos = 50
grid_thickness = 2

flash_timer = 10
FL_end_frame = 0
FL_end_count = 0

grid_preview_grid_gap = 20

num_previews = 5
preview_h = 100
preview_w = 100

preview_cols = 4
preview_rows = 4

hold_piece_x = 100
hold_piece_y = 200
hold_piece_h_per_cell = 35
hold_piece_w_per_cell = 35

frame_rate = 60


arr = 0
sdr = 0
das = 6
gravity = 10

if gravity == 0:
    piece_timer = -1
else:
    piece_timer = 1000 / gravity

current_piece_location = [num_cols / 2 - 2, 0, 0]

piece_dict = {
    1: np.array([[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]),
    2: np.array([[0, 0, 0], [2, 2, 2], [0, 0, 2]]),
    3: np.array([[0, 0, 0], [3, 3, 3], [3, 0, 0]]),
    4: np.array([[0, 0, 0], [0, 4, 4], [4, 4, 0]]),
    5: np.array([[0, 0, 0], [5, 5, 0], [0, 5, 5]]),
    6: np.array([[6, 6], [6, 6]]),
    7: np.array([[0, 0, 0], [7, 7, 7], [0, 7, 0]]),
}

perms = set(permutations([1, 2, 3, 4, 5, 6, 7]))

def Generate_Bag_Constrained(perms, constraints):
    bags_list = []
    result = []

    if len(constraints) == 0:
        return random.choice(list(perms))

    numbags = constraints[len(constraints) - 1][0] + 1

    for i in range(numbags):
        bags_list.append([])
        for bag in perms:
            will_add = True
            for constraint in constraints:

                if constraint[0] == i:

                    bool_values = map(
                        lambda test: bag.index(test[0]) < bag.index(test[1]),
                        constraint[1],
                    )

                    if all(bool_values):
                        will_add = False

            if will_add:
                bags_list[i].append(bag)

    for bags in bags_list:
        result += list(random.choice(bags))
    return result


def init_game():

    global num_rows
    global num_cols
    global board_width
    global board_height

    pg.init()
    pg.font.init()
    pg.display.init

    pg.display.set_mode((screen_width, screen_height))
    surf = pg.display.get_surface()

    surf.blit(tetris_logo, (0, 0, 50, screen_height / 2 + 25))

    # Draw game grid

    pg.draw.rect(
        surf,
        (20, 20, 20),
        (
            board_x_pos - grid_thickness,
            board_y_pos - grid_thickness,
            board_width + 2 * grid_thickness,
            board_height + 2 * grid_thickness,
        ),
    )

    for i in range(num_cols):
        for j in range(num_rows):
            pg.draw.rect(
                surf,
                "black",
                (
                    board_x_pos + i * board_width / num_cols + grid_thickness,
                    board_y_pos + j * board_height / num_rows + grid_thickness,
                    board_width / num_cols - 2 * grid_thickness,
                    board_height / num_rows - 2 * grid_thickness,
                ),
            )

    # Draw preview grid
    preview_x = board_x_pos + board_width + grid_preview_grid_gap
    preview_y = board_y_pos - grid_thickness

    pg.draw.rect(
        surf,
        (20, 20, 20),
        (
            preview_x,
            preview_y,
            preview_w + 2 * grid_thickness,
            (preview_h * (num_previews - 1.25)) + 2 * grid_thickness,
        ),
    )

    # Minus 5 to get rid of redundant rows in preview grid

    for i in range(preview_cols):
        for j in range(preview_rows * num_previews - 5):
            pg.draw.rect(
                surf,
                "black",
                (
                    preview_x + i * preview_w / preview_cols + 2 * grid_thickness,
                    preview_y + j * preview_h / (preview_rows) + 2 * grid_thickness,
                    preview_w / preview_cols - 2 * grid_thickness,
                    preview_h / preview_rows - 2 * grid_thickness,
                ),
            )


def refill_bag(bag):
    next_bag = [1, 2, 3, 4, 5, 6, 7]
    random.shuffle(next_bag)
    return bag + next_bag


def spawn_piece(num, board_state, update_bag=True):

    global can_hold
    global piece_timer
    global bag

    if update_bag:
        if len(bag) > 10:
            bag = bag[1:]
        else:
            bag = bag[1:]
            bag = refill_bag(bag)

    spawn_previews()

    can_hold = True

    if gravity == 0:
        piece_timer = -1
    else:
        piece_timer = 1000 / gravity

    if not num == 6:
        current_piece_location = [int(num_cols / 2 - 2), 0, 0]
    else:
        current_piece_location = [int(num_cols / 2 - 1), 0, 0]

    if num == 1:
        board_state = spawn_I(board_state)
        current_piece = 1
    elif num == 2:
        board_state = spawn_L(board_state)
        current_piece = 2
    elif num == 3:
        board_state = spawn_J(board_state)
        current_piece = 3
    elif num == 4:
        board_state = spawn_Z(board_state)
        current_piece = 4
    elif num == 5:
        board_state = spawn_S(board_state)
        current_piece = 5
    elif num == 6:
        board_state = spawn_O(board_state)
        current_piece = 6
    else:
        board_state = spawn_T(board_state)
        current_piece = 7
    return board_state, current_piece_location, current_piece


def spawn_previews():
    global preview_grid

    preview_grid = np.zeros(np.shape(preview_grid))
    pos = 0

    for i in range(num_previews):
        piece_array = np.flip(piece_dict[bag[i]], 0)
        preview_grid[
            pos: pos + (np.shape(piece_array)[0]), 0: np.shape(piece_array)[1]
        ] = piece_array
        if bag[i] == 6:
            pos += 1
        if bag[i] == 1:
            pos -= 1
        pos += np.shape(piece_array)[0]


def spawn_I(board_state):
    if (
        (board_state[20, 3] == 0)
        & (board_state[20, 4] == 0)
        & (board_state[20, 5] == 0)
        & (board_state[20, 6] == 0)
    ):
        board_state[20, 3] = -1
        board_state[20, 4] = -1
        board_state[20, 5] = -1
        board_state[20, 6] = -1
    else:
        die()
    return board_state


def spawn_L(board_state):
    if (
        (board_state[20, 3] == 0)
        & (board_state[20, 4] == 0)
        & (board_state[20, 5] == 0)
        & (board_state[21, 5] == 0)
    ):
        board_state[20, 3] = -2
        board_state[20, 4] = -2
        board_state[20, 5] = -2
        board_state[21, 5] = -2
    else:
        die()
    return board_state


def spawn_J(board_state):
    if (
        (board_state[20, 3] == 0)
        & (board_state[20, 4] == 0)
        & (board_state[20, 5] == 0)
        & (board_state[21, 5] == 0)
    ):
        board_state[20, 3] = -3
        board_state[21, 3] = -3
        board_state[20, 4] = -3
        board_state[20, 5] = -3
    else:
        die()
    return board_state


def spawn_Z(board_state):
    if (
        (board_state[21, 3] == 0)
        & (board_state[21, 4] == 0)
        & (board_state[20, 4] == 0)
        & (board_state[20, 5] == 0)
    ):
        board_state[21, 3] = -4
        board_state[21, 4] = -4
        board_state[20, 4] = -4
        board_state[20, 5] = -4
    else:
        die()
    return board_state


def spawn_S(board_state):
    if (
        (board_state[20, 3] == 0)
        & (board_state[20, 4] == 0)
        & (board_state[21, 4] == 0)
        & (board_state[21, 5] == 0)
    ):
        board_state[20, 3] = -5
        board_state[20, 4] = -5
        board_state[21, 4] = -5
        board_state[21, 5] = -5
    else:
        die()
    return board_state


def spawn_O(board_state):
    if (
        (board_state[20, 4] == 0)
        & (board_state[21, 4] == 0)
        & (board_state[20, 5] == 0)
        & (board_state[21, 5] == 0)
    ):
        board_state[20, 4] = -6
        board_state[21, 4] = -6
        board_state[20, 5] = -6
        board_state[21, 5] = -6
    else:
        die()
    return board_state


def spawn_T(board_state):
    if (
        (board_state[20, 3] == 0)
        & (board_state[20, 4] == 0)
        & (board_state[21, 4] == 0)
        & (board_state[20, 5] == 0)
    ):
        board_state[20, 3] = -7
        board_state[20, 4] = -7
        board_state[21, 4] = -7
        board_state[20, 5] = -7
    else:
        die()
    return board_state


def lock_active_piece(board_state, current_piece_location):
    global bag
    global piece_timer
    global forty_lines_count
    global num_pieces_placed

    num_pieces_placed += 1

    if gravity == 0:
        piece_timer = -1
    else:
        piece_timer = 1000 / gravity

    board_state = np.abs(board_state)
    board_state, count = line_clear(board_state)

    forty_lines_count += count
    if forty_lines_count >= 40 and (game_mode == 1):
        forty_lines_end()

    board_state, current_piece_location, current_piece = spawn_piece(
        bag[0], board_state
    )

    return board_state, current_piece_location, current_piece


def fall_tick(board_state, current_piece_location):
    global piece_timer

    current_piece = 0

    for i in range(num_cols):
        for j in range(num_rows):
            if board_state[j, i] < 0:
                current_piece = -board_state[j, i]

    board_state, current_piece_location_after = shift_down(
        board_state, current_piece_location
    )

    if not np.array_equal(current_piece_location_after, current_piece_location):
        piece_timer += 50 / gravity

    for i in range(num_cols):
        for j in range(num_rows):
            if piece_timer < 0:
                if board_state[j, i] < 0:
                    if j == 0:
                        (
                            board_state,
                            current_piece_location_after,
                            current_piece,
                        ) = lock_active_piece(board_state, current_piece_location)

                    if board_state[j - 1, i] > 0:
                        (
                            board_state,
                            current_piece_location_after,
                            current_piece,
                        ) = lock_active_piece(board_state, current_piece_location)

    return board_state, current_piece_location_after, current_piece


def die():
    board_state, current_piece_location, current_piece, hold_piece, frame_num = reset()


def shift_left(board_state, current_piece_location):
    coords = []
    for i in range(num_cols):
        for j in range(num_rows):
            if board_state[j, i] < 0:
                coords.append([j, i])
                if i == 0:
                    return board_state, current_piece_location
                if board_state[j, i - 1] > 0:
                    return board_state, current_piece_location

    for coord in coords:
        x = coord[1]
        y = coord[0]
        board_state[y, x] = 0
        board_state[y, x - 1] = -current_piece
    current_piece_location[0] -= 1
    return board_state, current_piece_location


def shift_right(board_state, current_piece_location):
    coords = []
    for i in range(num_cols):
        for j in range(num_rows):
            if board_state[j, num_cols - 1 - i] < 0:
                coords.append([j, i])
                if i == 0:
                    return board_state, current_piece_location
                if board_state[j, num_cols - i] > 0:
                    return board_state, current_piece_location

    for coord in coords:
        x = coord[1]
        y = coord[0]
        board_state[y, num_cols - x - 1] = 0
        board_state[y, num_cols - x] = -current_piece
    current_piece_location[0] += 1
    return board_state, current_piece_location


def shift_down(board_state, current_piece_location):

    coords = []
    coord_append = coords.append

    for i in range(num_cols):
        for j in range(num_rows):
            if board_state[j, i] < 0:
                coord_append([j, i])
                if j == 0:
                    return board_state, current_piece_location

                if board_state[j - 1, i] > 0:
                    return board_state, current_piece_location

    for coord in coords:
        x = coord[1]
        y = coord[0]
        if board_state[y - 1, x] == 0:
            board_state[y, x] = 0
            board_state[y - 1, x] = -current_piece
    current_piece_location[1] += 1

    return board_state, current_piece_location


def rotate(board_state, current_piece_location, direction):
    # Left is negative, right positive

    current_piece_location[2] += direction
    will_move = True
    current_piece_array = -piece_dict[current_piece]
    arr_h = np.shape(current_piece_array)[0]
    rotated_array = np.rot90(current_piece_array, current_piece_location[2])

    prev_rotation_array = np.rot90(
        current_piece_array, current_piece_location[2] - direction
    )

    eval_array = np.zeros(np.shape(rotated_array))

    for i in range((np.shape(rotated_array)[0])):
        for j in range((np.shape(rotated_array)[1])):
            if not (rotated_array[i, j] == 0) and not (
                rotated_array[i, j] == prev_rotation_array[i, j]
            ):
                eval_array[i, j] = rotated_array[i, j]
            else:
                eval_array[i, j] = 0

    eval_array = np.flipud(eval_array)

    for i in range((np.shape(rotated_array)[0])):
        for j in range((np.shape(rotated_array)[1])):
            if not (eval_array[j, i] == 0):
                array_location_y = num_rows - current_piece_location[1] - 1
                array_location_x = current_piece_location[0]
                # THIS CHECK SUCKS
                if (
                    (current_piece_location[0] < 0)
                    or (
                        current_piece_location[0]
                        > num_cols - np.shape(rotated_array)[1]
                    )
                    or (array_location_y - j < 0)
                ):
                    will_move = False
                elif not (board_state[array_location_y - j, array_location_x + i] == 0):
                    will_move = False

    if will_move:
        for i in range((np.shape(rotated_array)[0])):
            for j in range((np.shape(rotated_array)[1])):
                if not (prev_rotation_array[j, i] == 0):
                    board_state[
                        (num_rows - current_piece_location[1] - arr_h) + j,
                        current_piece_location[0] + i,
                    ] = 0

        for i in range((np.shape(rotated_array)[0])):
            for j in range((np.shape(rotated_array)[1])):
                if not (rotated_array[j, i] == 0):
                    board_state[
                        (num_rows - current_piece_location[1] - arr_h) + j,
                        current_piece_location[0] + i,
                    ] = rotated_array[j, i]

    else:
        board_state, current_piece_location = kick(
            board_state, current_piece_location, direction
        )

    return board_state, current_piece_location


def kick(board_state, current_piece_location, direction):
    # Create notation string
    notation_string = (
        str((current_piece_location[2] - direction) % 4)
        + ">>"
        + str(current_piece_location[2] % 4)
    )
    if current_piece == 1:
        test_list = kicktables.kick_tables_I[notation_string]
    else:
        test_list = kicktables.kick_tables[notation_string]

    # define array with desired rotation and "Current/Prev" rotation

    rotated_array = np.rot90(-piece_dict[current_piece], current_piece_location[2])
    prev_rotation_array = np.rot90(
        -piece_dict[current_piece], current_piece_location[2] - direction
    )

    arr_h = np.shape(rotated_array)[0]
    arr_w = np.shape(rotated_array)[1]

    array_location_y = num_rows - current_piece_location[1] - 1
    array_location_x = current_piece_location[0]

    rotated_array = np.flipud(rotated_array)
    prev_rotation_array = np.flipud(prev_rotation_array)

    for test in test_list:
        passed = True
        for i in range(arr_w):
            for j in range(arr_h):
                if rotated_array[j, i] < 0:
                    projected_cell_y = array_location_y - j + test[1]
                    projected_cell_x = array_location_x + i + test[0]

                    if (
                        (projected_cell_y < 0)
                        or (projected_cell_y > num_rows - 1)
                        or (projected_cell_x < 0)
                        or (projected_cell_x > num_cols - 1)
                    ):
                        passed = False
                    elif board_state[projected_cell_y, projected_cell_x] > 0:
                        passed = False

        if passed:
            for i in range((np.shape(rotated_array)[1])):
                for j in range((np.shape(rotated_array)[0])):
                    if not (prev_rotation_array[j, i] == 0):
                        board_state[array_location_y - j, array_location_x + i] = 0

            for i in range((np.shape(rotated_array)[1])):
                for j in range((np.shape(rotated_array)[0])):
                    projected_cell_y = array_location_y - j + test[1]
                    projected_cell_x = array_location_x + i + test[0]
                    if not (rotated_array[j, i] == 0):
                        board_state[projected_cell_y, projected_cell_x] = rotated_array[
                            j, i
                        ]

            current_piece_location[0] += test[0]
            current_piece_location[1] -= test[1]
            return board_state, current_piece_location

    return board_state, current_piece_location


def render_board(board_state):
    # Render game board
    global flash_timer
    global game_mode

    surface = pg.display.get_surface()

    draw_rect = pg.draw.rect

    colour_dict = {
        0: (0, 0, 0),
        1: (0, 153, 230),
        2: (200, 100, 0),
        3: (0, 0, 150),
        4: (200, 0, 0),
        5: (0, 180, 0),
        6: (200, 200, 0),
        7: (150, 0, 150),
        8: (40, 40, 40),
    }

    # Draw game grid
    if flash_timer >= 0:
        surface.fill((0, 0, 0))

    draw_rect(
        surface,
        (20, 20, 20),
        (
            board_x_pos - grid_thickness,
            board_y_pos - grid_thickness,
            board_width + 2 * grid_thickness,
            board_height + 2 * grid_thickness,
        ),
    )

    coords = []
    if (
        not (opener == 0)
        and (guide_on)
        and (num_pieces_placed / 7 < len(openers[opener]["Sample"]))
    ):

        coord_append = coords.append
        guide_board = openers[opener]["Sample"][int((num_pieces_placed) / 7)]
        board_copy = copy.deepcopy(board_state).clip(min=0)

        loc_copy = copy.deepcopy(current_piece_location)
        for i in range(num_cols):
            for j in range(num_rows):
                if guide_board[j, i] == current_piece:
                    coord_append([j, i])
                    board_copy[j, i] = -current_piece
        board_copyB = copy.deepcopy(board_copy)
        board_copy, loc_copy = shift_down(board_copy, loc_copy)
        if np.array_equal(board_copy, board_copyB):
            for coord in coords:
                x = coord[1]
                y = coord[0]
                draw_rect(
                    surface,
                    (255, 255, 255),
                    (
                        board_x_pos + x * board_width / num_cols + grid_thickness,
                        board_y_pos
                        + (num_rows - 1 - y) * board_height / num_rows
                        + grid_thickness,
                        board_width / num_cols - 2 * grid_thickness,
                        board_height / num_rows - 2 * grid_thickness,
                    ),
                )
        else:
            coords = []

    for i in range(num_cols):
        for j in range(num_rows):
            colour = colour_dict[abs(board_state[j, i])]
            if not (([j, i] in coords) and (colour == (0, 0, 0))):
                draw_rect(
                    surface,
                    colour,
                    (
                        board_x_pos + i * board_width / num_cols + grid_thickness,
                        board_y_pos
                        + (num_rows - 1 - j) * board_height / num_rows
                        + grid_thickness,
                        board_width / num_cols - 2 * grid_thickness,
                        board_height / num_rows - 2 * grid_thickness,
                    ),
                )

    # Draw preview grid
    preview_x = board_x_pos + board_width + grid_preview_grid_gap
    preview_y = board_y_pos - grid_thickness

    draw_rect(
        surface,
        (20, 20, 20),
        (
            preview_x,
            preview_y,
            preview_w + 2 * grid_thickness,
            (preview_h * (num_previews - 1.25)) + 2 * grid_thickness,
        ),
    )

    # Render preview board

    preview_x = board_x_pos + board_width + grid_preview_grid_gap
    preview_y = board_y_pos - grid_thickness

    for i in range(preview_cols):
        for j in range(preview_rows * num_previews - 5):
            colour = colour_dict[abs(preview_grid[j, i])]
            draw_rect(
                surface,
                colour,
                (
                    preview_x + i * preview_w / preview_cols + 2 * grid_thickness,
                    preview_y + j * preview_h / (preview_rows) + 2 * grid_thickness,
                    preview_w / preview_cols - 2 * grid_thickness,
                    preview_h / preview_rows - 2 * grid_thickness,
                ),
            )

    # Render Hold piece
    draw_rect(
        surface,
        (0, 0, 0),
        (
            hold_piece_x,
            hold_piece_y,
            hold_piece_w_per_cell * 4 + 2 * grid_thickness,
            hold_piece_h_per_cell * 4 + 2 * grid_thickness,
        ),
    )

    if not (hold_piece == 0):
        colour = colour_dict[hold_piece]
        hold_array = piece_dict[hold_piece]
        hold_array = np.flipud(hold_array)
        hold_arr_shape = np.shape(hold_array)

        for i in range(hold_arr_shape[1]):
            for j in range(hold_arr_shape[0]):
                if hold_array[j, i] == hold_piece:
                    draw_rect(
                        surface,
                        colour,
                        (
                            hold_piece_x + i * hold_piece_w_per_cell,
                            hold_piece_y + j * hold_piece_h_per_cell,
                            hold_piece_w_per_cell - 2 * grid_thickness,
                            hold_piece_h_per_cell - 2 * grid_thickness,
                        ),
                    )

        # Render guide piece

    # Render text

    # render_text(frame_num,forty_lines_count)

    # Render flash
    if flash_timer > 0:
        flash((0, 255, 0))
        flash_timer -= 1
    elif flash_timer == 0:
        surface.blit(tetris_logo, (0, 0, 50, screen_height / 2 + 25))

        flash_timer -= 1


def render_ghost_piece(board_state):
    surf = pg.display.get_surface()

    board_copy = copy.deepcopy(board_state)

    board_copy = soft_drop(board_copy, [0, 0, 0])[0]

    draw_rect = pg.draw.rect

    if not (np.array_equal(board_copy, board_state)):
        for i in range(num_cols):
            for j in range(num_rows):
                colour = pg.Color(40, 40, 40, a=10)
                if (board_copy[j, i] < 0) and (board_state[j, i] == 0):
                    draw_rect(
                        surf,
                        colour,
                        (
                            board_x_pos + i * board_width / num_cols + grid_thickness,
                            board_y_pos
                            + (num_rows - 1 - j) * board_height / num_rows
                            + grid_thickness,
                            board_width / num_cols - 2 * grid_thickness,
                            board_height / num_rows - 2 * grid_thickness,
                        ),
                    )


def soft_drop(board_state, loc):

    for i in range(num_rows):
        loc_before = copy.deepcopy(loc)
        board_state, loc_after = shift_down(board_state, loc)
        if np.array_equal(loc_after, loc_before):
            return board_state, loc
    return board_state, loc


def hard_drop(board_state, current_piece_location):

    global piece_timer

    board_state, current_piece_location = soft_drop(board_state, current_piece_location)
    piece_timer = -1
    board_state, current_piece_location, current_piece = fall_tick(
        board_state, current_piece_location
    )
    return board_state, current_piece_location, current_piece


def line_clear(board_state):

    board_shape = np.shape(board_state)

    cleared_lines = 0
    counter = 0

    while counter < board_shape[0]:

        if all(el > 0 for el in board_state[counter, :]):
            cleared_lines += 1
            board_state[counter: board_shape[0] - 1, :] = board_state[
                counter + 1: board_shape[0], :
            ]
            board_state[board_shape[0] - 1, :] = np.zeros([1, board_shape[1]])
            counter = -1
        counter += 1
    return board_state, cleared_lines


def hold(board_state, piece_to_hold):
    global bag
    global hold_piece

    board_state = board_state.clip(min=0)

    if hold_piece == 0:
        board_state, current_piece_location, current_piece = spawn_piece(
            bag[0], board_state
        )
    else:
        board_state, current_piece_location, current_piece = spawn_piece(
            hold_piece, board_state, update_bag=False
        )

    hold_piece = piece_to_hold

    can_hold = False
    return board_state, current_piece, current_piece_location, can_hold


def start_bag(opener):

    bag = list(Generate_Bag_Constrained(perms, openers[opener]["Constraints"]))
    return bag


def reset():
    global board_state
    global preview_grid
    global bag
    global hold_piece
    global frame_num
    global current_piece
    global game_mode
    global num_pieces_placed

    num_pieces_placed = 0

    game_mode = 0

    key_down_dict[pg.K_r] = 1

    board_state = np.zeros([num_rows, num_cols])

    preview_grid = np.zeros([preview_rows * num_previews, preview_cols])

    bag = start_bag(opener)
    hold_piece = 0
    frame_num = 0

    current_piece = bag[0]
    board_state, current_piece_location, current_piece = spawn_piece(
        current_piece, board_state
    )

    return board_state, current_piece_location, current_piece, hold_piece, frame_num


def forty_lines_start():
    global game_mode
    global forty_lines_count
    global frame_num
    global flash_timer

    board_state, current_piece_location, current_piece, hold_piece, frame_num = reset()

    frame_num = -30
    game_mode = 1
    forty_lines_count = 0

    return board_state, current_piece_location, current_piece, hold_piece, frame_num


def flash(colour):
    # IMPLEMENT THIS
    surf = pg.display.get_surface()
    flash_surf = surf.copy()
    flash_surf.fill(colour)
    flash_surf.set_alpha((flash_timer * 255 / 10))
    surf.blit(flash_surf, (0, 0))


def forty_lines_end():
    global game_mode
    global frame_num
    global FL_end_frame
    global FL_end_count

    game_mode = 2
    FL_end_frame = frame_num
    FL_end_count = forty_lines_count


def convertTime(mytime):

    if mytime < 0:
        secs = str(-round((1 / 60 * abs(mytime)) % 60, 3))
    else:
        secs = str(round((1 / 60 * mytime) % 60, 3))
    mins = int((1 / 60 * mytime) / 60)

    if abs(mytime / 60) % 60 < 10:
        secs = "0" + secs

    return str(mins) + ":" + secs


def render_text(mytime, lines_cleared, opener, arr, das, sdr):

    Font = "comic sans"
    font_size = 20

    surf = pg.display.get_surface()
    myfont = pg.font.SysFont(Font, font_size)
    opener_text = myfont.render(
        openers[opener]["Name"] + "  [Q]", False, (255, 255, 255)
    )
    myfont = pg.font.SysFont(Font, font_size)
    arr_text = myfont.render("arr: " + str(arr), False, (255, 255, 255))
    das_text = myfont.render("das: " + str(das), False, (255, 255, 255))
    sdr_text = myfont.render("sdr: " + str(sdr), False, (255, 255, 255))

    draw_rect = pg.draw.rect

    draw_rect(surf, (0, 0, 0), (0, 500, board_x_pos - 100, 300))

    if game_mode == 1:
        draw_rect(surf, (0, 0, 0), (board_x_pos + board_width + 50, 600, 200, 200))
        draw_rect(surf, (0, 0, 0), (board_x_pos - 100, 600, 100, 100))

        timer = myfont.render(convertTime(mytime), False, (255, 255, 255))
        num_lines = myfont.render(str(lines_cleared) + "/40", False, (255, 255, 255))

        surf.blit(timer, (board_x_pos + board_width + 50, 600))
        surf.blit(num_lines, (board_x_pos - 150, 600))

    if game_mode == 2:
        draw_rect(surf, (0, 0, 0), (board_x_pos + board_width + 50, 600, 200, 200))
        draw_rect(surf, (0, 0, 0), (board_x_pos - 100, 600, 100, 100))

        timer = myfont.render(convertTime(FL_end_frame), False, (255, 255, 255))
        num_lines = myfont.render(str(FL_end_count) + "/40", False, (255, 255, 255))

        surf.blit(timer, (board_x_pos + board_width + 50, 600))
        surf.blit(num_lines, (board_x_pos - 150, 600))

    surf.blit(opener_text, (10, 700))
    surf.blit(arr_text, (25, 500))
    surf.blit(das_text, (25, 550))
    surf.blit(sdr_text, (25, 600))


board_state = np.zeros([num_rows, num_cols])

preview_grid = np.zeros([preview_rows * num_previews, preview_cols])

key_down_dict = {
    pg.K_DOWN: 0,
    pg.K_UP: 0,
    pg.K_LEFT: 0,
    pg.K_RIGHT: 0,
    pg.K_z: 0,
    pg.K_x: 0,
    pg.K_a: 0,
    pg.K_SPACE: 0,
    pg.K_LSHIFT: 0,
    pg.K_c: 0,
    pg.K_r: 0,
}


init_game()

time_0 = time.time()
clock_flag = True

opener = 0

num_pieces_placed = 0

bag = start_bag(opener)


hold_piece = 0

current_piece = bag[0]
board_state, current_piece_location, current_piece = spawn_piece(
    current_piece, board_state
)

game_mode = 0
frame_num = 0
forty_lines_count = 0
render_board(board_state)
render_ghost_piece(board_state)
can_hold = True

time_list = []

pg.mixer.music.load(os.path.join("assets", "tetris_theme_cello_qtet.mp3"))
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.02)


pg.event.set_allowed([pg.KEYDOWN])

play_game = True

while play_game:

    # 60 FPS clock, game logic is called each frame
    elapsed_time = time.time() - time_0

    if (
        (elapsed_time - (1 / frame_rate) / 2) % (1 / frame_rate) < 1 / (10 * frame_rate)
    ) and (clock_flag is False):

        clock_flag = True

        if not ((frame_num >= 0) and (frame_num <= 11)):

            render_text(frame_num, forty_lines_count, opener, arr, das, sdr)

        pg.display.flip()

    if (elapsed_time % (1 / frame_rate) < 1 / (10 * frame_rate)) and (
        clock_flag is True
    ):

        frame_num += 1
        clock_flag = False

        # Game logic

        # tick piece timer

        piece_timer -= 1

        # Get held keys

        all_keys = pg.key.get_pressed()

        # Get list of events and do stuff accordingly
        if gravity == 0:
            pass
        elif (frame_num % round(100 / gravity) == 0) and (
            key_down_dict[pg.K_DOWN]
        ) == 0:
            board_state, current_piece_location, current_piece = fall_tick(
                board_state, current_piece_location
            )
            render_board(board_state)
            render_ghost_piece(board_state)
        # Render any text that should be on screen

        ev = pg.event.get()

        if frame_num == 0:

            flash_timer = 10

        if (frame_num >= 0) and (frame_num <= 11):
            render_board(board_state)
            render_ghost_piece(board_state)

        for event in ev:

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_LSHIFT:
                    key_down_dict[pg.K_LSHIFT] = 1
                    if frame_num >= 0:
                        if can_hold:
                            (
                                board_state,
                                current_piece,
                                current_piece_location,
                                can_hold,
                            ) = hold(board_state, current_piece)
                        render_board(board_state)
                        render_ghost_piece(board_state)
                        continue
                if event.key == pg.K_c:
                    key_down_dict[pg.K_c] = 1
                    if frame_num >= 0:
                        if can_hold:
                            (
                                board_state,
                                current_piece,
                                current_piece_location,
                                can_hold,
                            ) = hold(board_state, current_piece)
                        render_board(board_state)
                        render_ghost_piece(board_state)
                        continue

                if event.key == pg.K_a:
                    key_down_dict[pg.K_a] = 1
                    if frame_num >= 0:
                        board_state, current_piece_location = rotate(
                            board_state, current_piece_location, 2
                        )
                        render_board(board_state)
                        render_ghost_piece(board_state)
                        continue

                if event.key == pg.K_DOWN:
                    key_down_dict[pg.K_DOWN] = 1
                    if frame_num >= 0:
                        if sdr == 0:
                            key_down_dict[pg.K_DOWN] = 1
                            board_state, current_piece_location = soft_drop(
                                board_state, current_piece_location
                            )
                            render_board(board_state)
                            render_ghost_piece(board_state)
                            continue

                        board_state, current_piece_location = shift_down(
                            board_state, current_piece_location
                        )
                        render_board(board_state)
                        render_ghost_piece(board_state)
                        continue
                if event.key == pg.K_LEFT:
                    key_down_dict[pg.K_LEFT] = 1
                    key_down_dict[pg.K_RIGHT] = 0
                    if frame_num >= 0:
                        board_state, current_piece_location = shift_left(
                            board_state, current_piece_location
                        )
                        render_board(board_state)
                        render_ghost_piece(board_state)
                        continue

                if event.key == pg.K_RIGHT:
                    key_down_dict[pg.K_RIGHT] = 1
                    key_down_dict[pg.K_LEFT] = 0
                    if frame_num >= 0:
                        board_state, current_piece_location = shift_right(
                            board_state, current_piece_location
                        )
                        render_board(board_state)
                        render_ghost_piece(board_state)
                        continue

                if event.key == pg.K_z:
                    key_down_dict[pg.K_z] = 1
                    if frame_num >= 0:
                        board_state, current_piece_location = rotate(
                            board_state, current_piece_location, -1
                        )
                        render_board(board_state)
                        render_ghost_piece(board_state)
                        continue

                if event.key == pg.K_x:
                    key_down_dict[pg.K_x] = 1
                    if frame_num >= 0:
                        board_state, current_piece_location = rotate(
                            board_state, current_piece_location, 1
                        )
                        render_board(board_state)
                        render_ghost_piece(board_state)
                        continue

                if event.key == pg.K_UP:
                    key_down_dict[pg.K_x] = 1
                    if frame_num >= 0:
                        board_state, current_piece_location = rotate(
                            board_state, current_piece_location, 1
                        )
                        render_board(board_state)
                        render_ghost_piece(board_state)
                        continue

                if event.key == pg.K_SPACE:
                    key_down_dict[pg.K_SPACE] = 1
                    if frame_num >= 0:
                        board_state, current_piece_location, current_piece = hard_drop(
                            board_state, current_piece_location
                        )
                        render_board(board_state)
                        render_ghost_piece(board_state)
                        continue
                if event.key == pg.K_r:
                    key_down_dict[pg.K_r] = 1
                    (
                        board_state,
                        current_piece_location,
                        current_piece,
                        hold_piece,
                        frame_num,
                    ) = reset()
                    render_board(board_state)
                    render_ghost_piece(board_state)
                    continue

                if event.key == pg.K_f:
                    key_down_dict[pg.K_f] = 1
                    (
                        board_state,
                        current_piece_location,
                        current_piece,
                        hold_piece,
                        frame_num,
                    ) = forty_lines_start()
                    render_board(board_state)
                    render_ghost_piece(board_state)
                    continue

                if event.key == pg.K_q:
                    opener += 1
                    opener = opener % len(openers)
                    render_board(board_state)
                    continue

                if event.key == pg.K_KP9:
                    arr += 1
                    render_board(board_state)
                    continue

                if event.key == pg.K_KP7:
                    arr -= 1
                    if arr < 0:
                        arr = 0
                    render_board(board_state)
                    continue

                if event.key == pg.K_KP6:
                    das += 1
                    render_board(board_state)
                    continue

                if event.key == pg.K_KP4:
                    das -= 1
                    if das < 0:
                        das = 0
                    render_board(board_state)
                    continue

                if event.key == pg.K_KP3:
                    sdr += 1
                    render_board(board_state)
                    continue

                if event.key == pg.K_KP1:
                    sdr -= 1
                    if sdr < 0:
                        sdr = 0
                    render_board(board_state)
                    continue

                if event.key == pg.K_ESCAPE:
                    play_game = False
                    continue

        # Check for held keys

        all_keys = pg.key.get_pressed()

        for myKey in key_down_dict:
            if (all_keys[myKey]) and (key_down_dict[myKey] > 0):
                key_down_dict[myKey] += 1
            else:
                key_down_dict[myKey] = 0

        # Do stuff with held keys

        # Checking if we should DAS

        if key_down_dict[pg.K_LEFT] > das:
            if frame_num >= 0:
                if arr == 0:
                    for i in range(9):
                        board_state, current_piece_location = shift_left(
                            board_state, current_piece_location
                        )

                elif (key_down_dict[pg.K_LEFT] - das) % arr == 0:
                    board_state, current_piece_location = shift_left(
                        board_state, current_piece_location
                    )
                render_board(board_state)
                render_ghost_piece(board_state)
                # pg.display.flip();
                continue

        if key_down_dict[pg.K_RIGHT] > das:
            if frame_num >= 0:
                if arr == 0:
                    for i in range(9):
                        board_state, current_piece_location = shift_right(
                            board_state, current_piece_location
                        )

                elif (key_down_dict[pg.K_RIGHT] - das) % arr == 0:
                    board_state, current_piece_location = shift_right(
                        board_state, current_piece_location
                    )
                render_board(board_state)
                render_ghost_piece(board_state)
                # pg.display.flip();
                continue

        # Checking if we should soft drop

        if key_down_dict[pg.K_DOWN] > 0:
            if frame_num >= 0:
                if sdr == 0:
                    board_state, current_piece_location = soft_drop(
                        board_state, current_piece_location
                    )
                    render_board(board_state)
                elif key_down_dict[pg.K_DOWN] % round(100 / sdr) == 0:
                    board_state, current_piece_location = shift_down(
                        board_state, current_piece_location
                    )
                    render_board(board_state)
                    render_ghost_piece(board_state)
                    # pg.display.flip();
                    continue
