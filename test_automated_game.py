"""Sprint 3
Tests for the AutomatedGame class.
"""


import unittest
from automated_game import AutomatedGame


class TestAutomatedGame(unittest.TestCase):

    def test_auto_move_reduces_peg_count(self):
        # Arrange: Create a new automated game
        game = AutomatedGame(7, "English")
        initial_count = len(game.pegs)

        # Act: Let the computer make one move
        result = game.auto_move()

        # Assert: Move succeeds and removes one peg
        self.assertTrue(result)
        self.assertEqual(
            len(game.pegs),
            initial_count - 1
        )

    def test_autoplay_ends_game(self):
        # Arrange
        game = AutomatedGame(7, "English")

        # Act: Play automatically until finished
        game.autoplay()

        # Assert: The game has ended
        self.assertTrue(game.is_game_over())
        self.assertEqual(len(game.valid_moves()), 0)

    def test_auto_move_when_game_over(self):
        # Arrange: Create a finished game
        game = AutomatedGame(7, "English")

        # Leave only the center peg
        center = (3, 3)
        game.pegs = {center}

        # Act: Attempt an automatic move
        result = game.auto_move()

        # Assert: No move should be possible
        self.assertFalse(result)
        self.assertEqual(game.pegs, {center})

    def test_autoplay_hexagon_board(self):
        # Arrange: Create a Hexagon board
        game = AutomatedGame(7, "Hexagon")

        # Act: Play until finished
        game.autoplay()

        # Assert: The game reaches a terminal state
        self.assertTrue(game.is_game_over())


if __name__ == "__main__":
    unittest.main()