"""Sprint 3
Tests for the GameRecorder class.
"""
import os
import tempfile
import unittest

from game import PegSolitaire
from game_record import GameRecorder


class TestGameRecorder(unittest.TestCase):

    def test_save_and_replay_game(self):
        game = PegSolitaire(7, "English")
        recorder = GameRecorder(game)

        start = (3, 1)
        end = (3, 3)

        # Make and record a valid move
        self.assertTrue(game.make_move(start, end))
        recorder.record_move(start, end)

        # Create a temporary text file
        with tempfile.TemporaryDirectory() as folder:
            filename = os.path.join(folder, "recording.txt")

            # Save the recording
            recorder.save_game(filename)

            # Replay it into a new game
            replayed_game = GameRecorder.replay_game(filename)

        # Both games should have identical board states
        self.assertEqual(game.size, replayed_game.size)
        self.assertEqual(game.board_type, replayed_game.board_type)
        self.assertEqual(game.pegs, replayed_game.pegs)

    def test_save_game_creates_file(self):
        game = PegSolitaire(7, "English")
        recorder = GameRecorder(game)

        with tempfile.TemporaryDirectory() as folder:
            filename = os.path.join(folder, "recording.txt")

            recorder.save_game(filename)

            self.assertTrue(os.path.exists(filename))

    def test_invalid_recorded_move_is_rejected(self):
        game = PegSolitaire(7, "English")
        recorder = GameRecorder(game)

        # Record a move that cannot legally occur
        recorder.record_move((0, 0), (0, 2))

        with tempfile.TemporaryDirectory() as folder:
            filename = os.path.join(folder, "recording.txt")

            recorder.save_game(filename)

            with self.assertRaises(ValueError):
                GameRecorder.replay_game(filename)


if __name__ == "__main__":
    unittest.main()