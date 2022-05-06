from enum import Enum

class Tetronimoes(Enum):
    I = 1
    S = 2
    Z = 3
    T = 4
    L = 5
    J = 6
    O = 7

tetronimo_colours = {
    Tetronimoes.I: (0, 153, 230),
    Tetronimoes.J: (200, 100, 0),
    Tetronimoes.L: (0, 0, 150),
    Tetronimoes.Z: (200, 0, 0),
    Tetronimoes.S: (0, 180, 0),
    Tetronimoes.O: (200, 200, 0),
    Tetronimoes.T: (150, 0, 150),
}
