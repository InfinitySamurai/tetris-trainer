import random
from bag import Bag

from data.tetronimoData import Tetronimoes
from tetronimo import Tetronimo


class BagManager():
    def __init__(self, settings):
        self.settings = settings
        self.current_bag = Bag(settings)
        self.future_bags = [Bag(settings)]
        return
    
    def fetch_piece(self):
        next_piece =  self.current_bag.contents.pop(0)

        if len(self.current_bag.contents) == 0:
            self.current_bag = self.future_bags.pop(0)

        return next_piece