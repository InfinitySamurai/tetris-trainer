from typing import Dict

colours = {
    "grid": (20, 20, 20),
}

gameSettings: Dict[str, float] = {
    "screen_width": 1000,
    "screen_height": 800,
    "board_y_pos": 50,
    "board_width": 300,
    "board_height": 700,
    "num_cols": 10,
    "num_rows": 22,
    "grid_thickness": 2,
    "preview_gap_from_main_grid": 20,
    "preview_count": 5
}



def get_game_settings():
    settings = gameSettings.copy()
    settings["board_x_pos"] = gameSettings["screen_width"] / 2 - gameSettings["board_width"] / 2
    return settings
