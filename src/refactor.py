
import game
import os
import pygame as pg

from data.settings import get_game_settings, colours
from input import InputController, Inputs
from tickManager import TickManager

gameSettings = get_game_settings()

pg.init()
pg.font.init()
pg.display.init
pg.display.set_mode((gameSettings["screen_width"], gameSettings["screen_height"]))

tetris_logo = pg.image.load(os.path.join("assets", "tetris.png"))

game = game.Game(gameSettings)

input_controller = InputController()
tick_manager = TickManager(gameSettings["frames_per_second"])

game_surface = pg.display.get_surface()

while True:
    pg.event.pump()
    input_map = input_controller.get_input()
    if input_map[Inputs.EXIT] is True:
        exit()

    tick_manager.update()
    if tick_manager.has_ticked():
        game.update(input_map)

    game_surface.fill(colours["background"])
    game_surface.blit(tetris_logo, (0, 0, 50, gameSettings["screen_height"] / 2 + 25))
    game.draw(game_surface)
    pg.display.flip()