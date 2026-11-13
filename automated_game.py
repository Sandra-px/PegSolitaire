"""
This is an automated game for Peg Solitaire.
Sprint 3
"""

import random
from game import PegSolitaire

class AutomatedGame(PegSolitaire):
    """controled via computer"""

    def auto_move(self):
        moves = self.valid_moves()

        if not moves:
            return False

        start, end = random.choice(moves)
        result = self.make_move(start, end)

        if result:
            self.last_move = (start, end)

        return result

    def autoplay(self):
        while not self.is_game_over():
            if not self.auto_move():
                break