
import game
import os
import pygame as pg
from data.settings import get_game_settings
from input import InputController, Inputs

gameSettings = get_game_settings()

## CHECK THIS ALEX

pg.init()
pg.font.init()
pg.display.init
pg.display.set_mode((gameSettings["screen_width"], gameSettings["screen_height"]))

tetris_logo = pg.image.load(os.path.join("assets", "tetris.png"))

game = game.Game(gameSettings)

inputController = InputController()

game_surface = pg.display.get_surface()
game_surface.blit(tetris_logo, (0, 0, 50, gameSettings["screen_height"] / 2 + 25))


while True:
    pg.event.pump()

    input_map = inputController.get_input()

    if input_map[Inputs.EXIT] is True:
        exit()

    game.draw(game_surface)
    pg.display.flip()
