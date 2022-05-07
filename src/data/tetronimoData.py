from enum import Enum
import numpy as np

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
    Tetronimoes.J: (0, 0, 150),
    Tetronimoes.L: (200, 100, 0),
    Tetronimoes.S: (200, 0, 0),
    Tetronimoes.Z: (0, 180, 0),
    Tetronimoes.O: (200, 200, 0),
    Tetronimoes.T: (150, 0, 150),
}

tetronimo_shapes = {
    Tetronimoes.I: np.array([[0, 0, 0, 0], [Tetronimoes.I.value, Tetronimoes.I.value, Tetronimoes.I.value, Tetronimoes.I.value], [0, 0, 0, 0], [0, 0, 0, 0]]),
    Tetronimoes.J: np.array([[Tetronimoes.J.value, 0, 0], [Tetronimoes.J.value, Tetronimoes.J.value, Tetronimoes.J.value], [0, 0, 0]]),
    Tetronimoes.L: np.array([[0, 0, Tetronimoes.L.value], [Tetronimoes.L.value, Tetronimoes.L.value, Tetronimoes.L.value], [0, 0, 0]]),
    Tetronimoes.S: np.array([[0, Tetronimoes.S.value, Tetronimoes.S.value], [Tetronimoes.S.value, Tetronimoes.S.value, 0], [0, 0, 0]]),
    Tetronimoes.Z: np.array([[Tetronimoes.Z.value, Tetronimoes.Z.value, 0], [0, Tetronimoes.Z.value, Tetronimoes.Z.value], [0, 0, 0]]),
    Tetronimoes.O: np.array([[Tetronimoes.O.value, Tetronimoes.O.value], [Tetronimoes.O.value, Tetronimoes.O.value]]),
    Tetronimoes.T: np.array([[0, Tetronimoes.T.value, 0], [Tetronimoes.T.value, Tetronimoes.T.value, Tetronimoes.T.value], [0, 0, 0]]),
}