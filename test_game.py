"""
test_game.py
 
Sprint 2
"""
import unittest
from game import PegSolitaire

class TestPegSolitaire(unittest.TestCase):
    def test_new_game_initialization(self):
        game = PegSolitaire(7, 'English')
        self.assertNotIn((3,3), game.pegs)
        self.assertEqual(len(game.cells)-1, len(game.pegs))

    def test_valid_move_removes_jumped_peg(self):
        game = PegSolitaire(7, 'English')
        self.assertTrue(game.make_move((3,1), (3,3)))
        self.assertNotIn((3,1), game.pegs)
        self.assertNotIn((3,2), game.pegs)
        self.assertIn((3,3), game.pegs)

    def test_invalid_move_does_not_change_board(self):
        game = PegSolitaire()
        before = game.pegs.copy()
        self.assertFalse(game.make_move((0,0),(3,3)))
        self.assertEqual(before,game.pegs)

    def test_all_board_types_initialize(self):
        for kind in PegSolitaire.TYPES:
            with self.subTest(kind=kind):
                game=PegSolitaire(7,kind)
                self.assertIn((3,3),game.cells)
                self.assertNotIn((3,3),game.pegs)

    def test_invalid_size_rejected(self):
        with self.assertRaises(ValueError):
            PegSolitaire(4,'English')

    def test_game_over_when_no_moves(self):
        game=PegSolitaire()
        game.pegs={(0,2),(6,4)}
        self.assertTrue(game.is_game_over())
        self.assertEqual('Very Good',game.rating())

    def test_game_over_one_peg(self):
        game=PegSolitaire()
        game.pegs={(3,3)}
        self.assertTrue(game.is_game_over())
        self.assertEqual('Outstanding',game.rating())

if __name__=='__main__':
    unittest.main()
