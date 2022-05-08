from typing import Any, Dict

colours = {"grid": (20, 20, 20), "background": (0, 0, 0), "debug_green": (0, 255, 0)}

gameSettings: Dict[str, Any] = {
    "debug": True,
    "screen_width": 1000,
    "screen_height": 800,
    "board_y_pos": 50,
    "board_width": 300,
    "board_height": 700,
    "num_cols": 10,
    "num_rows": 22,
    "cell_size": 30,
    "grid_thickness": 3,
    "preview_gap_from_main_grid": 20,
    "preview_count": 5,
    "held_piece_x_pos": 100,
    "held_piece_y_pos": 300,
    "held_piece_box_offset": 50,
    "frames_per_second": 60,
    "start_gravity": 0.05,
    "lock_ticks": 120,
    "lock_max_rotations": 15,
}

# settings are in frames
player_settings = {
    "delayed_auto_shift": 15,
    "automatic_repeat_rate": 2,
    "soft_drop_factor": 20,
}


def get_game_settings():
    settings = gameSettings.copy()
    settings["board_x_pos"] = (
        gameSettings["screen_width"] / 2 - gameSettings["board_width"] / 2
    )
    settings["board_width"] = (
        gameSettings["cell_size"] + gameSettings["grid_thickness"]
    ) * gameSettings["num_cols"]
    settings["preview_x_pos"] = (
        settings["board_x_pos"]
        + settings["board_width"]
        + settings["preview_gap_from_main_grid"]
    )
    return settings
