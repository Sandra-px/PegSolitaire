"""
Manual game for Peg Solitaire.
This module contains the logic for playing Peg Solitaire manually
Sprint 3
"""

import random
from game import PegSolitaire

class ManualGame(PegSolitaire):
    """Manual game class for Peg Solitaire."""
    def make_player_move(self, start, end):
        return self.make_move(start, end)

    """program can make up to 3 random moves, player continues from resulting state"""
    def randomize(self, number_of_moves=3):
        moves_performed = 0 
        for _ in range(number_of_moves):
            moves = self.valid_moves()

            if not moves:
                break
            start, end = random.choice(moves)

            if self.make_move(start, end):
                moves_performed += 1
        return moves_performed  
    