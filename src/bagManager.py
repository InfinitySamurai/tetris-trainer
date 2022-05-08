from bag import Bag

from data.tetronimoData import Tetronimoes
from tetronimo import Tetronimo


class BagManager():
    def __init__(self, settings):
        self.settings = settings
        self.current_bag = Bag(settings)
        self.future_bags = [Bag(settings), Bag(settings)]
        return
    
    def fetch_piece(self):
        next_piece =  self.current_bag.contents.pop(0)

        if len(self.current_bag.contents) == 0:
            self.current_bag = self.future_bags.pop(0)
            self.future_bags.append(Bag(self.settings))
        

        return next_piece

    def peek_next_pieces(self, count: int):
        pieces_in_current_bag = len(self.current_bag.contents)
        current_bag_contents = self.current_bag.contents
        if pieces_in_current_bag > count:
            return current_bag_contents[:count]
        
        overflow_bag_contents = self.future_bags[0].contents
        overflow_pieces = count - pieces_in_current_bag
        return current_bag_contents.copy() + overflow_bag_contents[:overflow_pieces]