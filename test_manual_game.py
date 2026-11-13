"""For sprint 3: Testing the ManualGame class."""

import unittest
from manual_game import ManualGame

class TestManualGame(unittest.TestCase):
    def test_randomize_reduces_peg_count(self):
        game = ManualGame(7, 'English')
        initial_count = len(game.pegs)
        moves = game.randomize(3)
        self.assertEqual(
            len(game.pegs),
            initial_count - moves
        )

        self.assertGreater(moves, 0)

    def test_randomize_zero_moves(self):
        game = ManualGame(7, "English")

        initial_pegs = game.pegs.copy()

        moves = game.randomize(0)

        self.assertEqual(moves, 0)
        self.assertEqual(game.pegs, initial_pegs)

    def test_randomize_only_uses_valid_positions(self):
        game = ManualGame(7, "English")

        game.randomize(3)

        self.assertTrue(
            game.pegs.issubset(game.cells)
        )


if __name__ == "__main__":
    unittest.main()

