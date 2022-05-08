from enum import Enum
from typing import Tuple, Dict
import numpy as np

# Rotations are specifically in this order. CCW is a numpy 90 degree rotation
class Rotation(Enum):
    START = 0
    CCW = 1
    UPSIDEDOWN = 2
    CW = 3

possible_rotation_count = len(list(Rotation))

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

Kicktable = Dict[Tuple[int, int], list[Tuple[int, int]]]

# kick tables are (x, y) where positive x is right and positive y is up
kick_table_I: Kicktable = {
    (Rotation.START.value, Rotation.CW.value): [(-2,0),(1,0),(-2,-1),(1,2)],
    (Rotation.CW.value, Rotation.START.value): [(2,0),(-1,0),(2,1),(-1,-2)],
    (Rotation.CW.value, Rotation.UPSIDEDOWN.value): [(-1,0),(2,0),(-1,2),(2,-1)],
    (Rotation.UPSIDEDOWN.value, Rotation.CW.value): [(1,0),(-2,0),(1,-2),(-2,1)],
    (Rotation.UPSIDEDOWN.value, Rotation.CCW.value): [(2,0),(-1,0),(2,1),(-1,-2)],
    (Rotation.CCW.value, Rotation.UPSIDEDOWN.value): [(-2,0),(1,0),(-2,-1),(1,2)],
    (Rotation.CCW.value, Rotation.START.value): [(1,0),(-2,0),(1,-2),(-2,1)],
    (Rotation.START.value, Rotation.CCW.value): [(-1,0),(2,0),(-1,2),(2,-1)],
    (Rotation.START.value, Rotation.UPSIDEDOWN.value): [(0,1),(1,1),(-1,1),(1,0),(-1,0)],
    (Rotation.UPSIDEDOWN.value, Rotation.START.value): [(0,-1),(-1,-1),(1,-1),(-1,0),(1,0)],
    (Rotation.CW.value, Rotation.CCW.value): [(1,0),(1,2),(1,1),(0,2),(0,1)],
    (Rotation.CCW.value, Rotation.CW.value): [(-1,0),(-1,2),(-1,1),(0,2),(0,1)]
}

kick_table: Kicktable = {
    (Rotation.START.value, Rotation.CW.value): [(-1,0),(-1,1),(0,-2),(-1,-2)],
    (Rotation.CW.value, Rotation.START.value): [(1,0),(1,-1),(0,2),(1,2)],
    (Rotation.CW.value, Rotation.UPSIDEDOWN.value): [(1,0),(1,-1),(0,2),(1,2)],
    (Rotation.UPSIDEDOWN.value, Rotation.CW.value): [(-1,0),(-1,1),(0,-2),(-1,-2)],
    (Rotation.UPSIDEDOWN.value, Rotation.CCW.value): [(1,0),(1,1),(0,-2),(1,-2)],
    (Rotation.CCW.value, Rotation.UPSIDEDOWN.value): [(-1,0),(-1,-1),(0,2),(-1,2)],
    (Rotation.CCW.value, Rotation.START.value): [(-1,0),(-1,-1),(0,2),(-1,2)],
    (Rotation.START.value, Rotation.CCW.value): [(1,0),(1,1),(0,-2),(1,-2)],
    (Rotation.START.value, Rotation.UPSIDEDOWN.value): [(0,1),(1,1),(-1,1),(1,0),(-1,0)],
    (Rotation.UPSIDEDOWN.value, Rotation.START.value): [(0,-1),(-1,-1),(1,-1),(-1,0),(1,0)],
    (Rotation.CW.value, Rotation.CCW.value): [(1,0),(1,2),(1,1),(0,2),(0,1)],
    (Rotation.CCW.value, Rotation.CW.value): [(-1,0),(-1,2),(-1,1),(0,2),(0,1)]
}
