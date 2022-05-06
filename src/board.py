import pygame as pg
from data.settings import colours

class Board:

    def __init__(self, gameSettings):
        self.width = 10
        self.height = 20

        self.settings = gameSettings

    def draw(self, surface):
        self.draw_static(surface)

    def draw_static(self, surface):
        # background
        pg.draw.rect(
            surface,
            colours["grid"],
            (
                self.settings["board_x_pos"] - self.settings["grid_thickness"],
                self.settings["board_y_pos"] - self.settings["grid_thickness"],
                self.settings["board_width"] + 2 * self.settings["grid_thickness"],
                self.settings["board_height"] + 2 * self.settings["grid_thickness"],
            ),
        )

        # main stage grid
        for i in range(self.settings["num_cols"]):
            for j in range(self.settings["num_rows"]):
                pg.draw.rect(
                    surface,
                    "black",
                    (
                        self.settings["board_x_pos"] + i * self.settings["board_width"] / self.settings["num_cols"] + self.settings["grid_thickness"],
                        self.settings["board_y_pos"] + j * self.settings["board_height"] / self.settings["num_rows"] + self.settings["grid_thickness"],
                        self.settings["board_width"] / self.settings["num_cols"] - 2 * self.settings["grid_thickness"],
                        self.settings["board_height"] / self.settings["num_rows"] - 2 * self.settings["grid_thickness"],
                    ),
                )

        # preview grid
        # preview_x = self.settings["board_x_pos"] + self.settings["board_width"] + self.settings["preview_gap_from_main_grid"]
        # preview_y = self.settings["board_y_pos"] - self.settings["grid_thickness"]

        # pg.draw.rect(
        #     surface,
        #     colours["grid"],
        #     (
        #         preview_x,
        #         preview_y,
        #         self.settings["preview_width"] + 2 * self.settings["grid_thickness"],
        #         (self.settings["preview_height"] * (self.settings["preview_count"] - 1.25)) + 2 * self.settings["grid_thickness"],
        #     ),
        # )


def draw_grid(surface, posx, posy, num_cols, num_rows, grid_width, grid_height, line_width):
    for i in range(num_cols):
        pg.draw.line(surface, colours["grid"], (posx, posy), (posx + num_cols, posy))
        # for i in range(self.settings["num_cols"]):
        #     for j in range(self.settings["num_rows"]):
        #         pg.draw.rect(
        #             surface,
        #             "black",
        #             (
        #                 self.settings["board_x_pos"] + i * self.settings["board_width"] / self.settings["num_cols"] + self.settings["grid_thickness"],
        #                 self.settings["board_y_pos"] + j * self.settings["board_height"] / self.settings["num_rows"] + self.settings["grid_thickness"],
        #                 self.settings["board_width"] / self.settings["num_cols"] - 2 * self.settings["grid_thickness"],
        #                 self.settings["board_height"] / self.settings["num_rows"] - 2 * self.settings["grid_thickness"],
        #             ),
        #         )