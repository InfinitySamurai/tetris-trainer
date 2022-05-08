import random

from data.tetronimoData import Tetronimoes
from tetronimo import Tetronimo


class BagManager():
    def __init__(self, settings):
        self.settings = settings
        return
    
    def fetch_piece(self):
        return Tetronimo(random.choice(list(Tetronimoes)), (0, 0), self.settings)