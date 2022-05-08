import random

from data.tetronimoData import Tetronimoes
from tetronimo import Tetronimo

class Bag():
    def __init__(self, settings):
        self.contents = list(map(lambda tetronimo_type: Tetronimo(tetronimo_type, settings), Tetronimoes))
        random.shuffle(self.contents)

        return
