"""
Course: CS 449 - Software Engineering
Assignment: Peg Solitaire
Author: Sandra Pacheco
Date edited: 9/18/2026
File name: test_peg_move.py
 
Unit tests for peg_move.py, written with Python's built-in unittest
framework (xUnit-style: test classes inherit from unittest.TestCase).
 
Run with:
   py -m unittest test_peg_move.py -v
"""
 
import unittest
from peg_move import Position, midpoint, is_valid_move
 
 
class TestMidpoint(unittest.TestCase):
    def test_horizontal_midpoint(self):
        start = Position(2, 0)
        end = Position(2, 2)
        self.assertEqual(midpoint(start, end), Position(2, 1))
 
    def test_diagonal_midpoint(self):
        start = Position(0, 0)
        end = Position(2, 2)
        self.assertEqual(midpoint(start, end), Position(1, 1))
 
    def test_not_two_apart_returns_none(self):
        start = Position(0, 0)
        end = Position(0, 1)  # only one square away not a valid jump distance
        self.assertIsNone(midpoint(start, end))
 

if __name__ == "__main__":
    unittest.main()