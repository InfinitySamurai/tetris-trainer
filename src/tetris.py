
import game
import os
import pygame as pg

from data.settings import get_game_settings, colours, player_settings
from input import InputController, Inputs
from tickManager import TickManager

game_settings = get_game_settings()

pg.init()
pg.font.init()
pg.display.init
pg.display.set_mode((game_settings["screen_width"], game_settings["screen_height"]))

tetris_logo = pg.image.load(os.path.join("assets", "tetris.png"))

game = game.Game(game_settings)

input_controller = InputController(player_settings)
tick_manager = TickManager(game_settings["frames_per_second"])

game_surface = pg.display.get_surface()

while True:
    pg.event.pump()
    input_map = input_controller.get_input()
    if input_map[Inputs.EXIT]["held"] is True:
        exit()

    tick_manager.update()
    if tick_manager.has_ticked():
        input_controller.update()
        game.update(input_map, player_settings)

    game_surface.fill(colours["background"])
    game_surface.blit(tetris_logo, (0, 0, 50, game_settings["screen_height"] / 2 + 25))
    game.draw(game_surface)
    pg.display.flip()