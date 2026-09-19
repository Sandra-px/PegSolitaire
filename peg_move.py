"""
Course: CS 449 - Software Engineering
Assignment: Peg Solitaire
Author: Sandra Pacheco
Date edited: 9/17/2026
File name:peg_move.py
 
A small, reusable piece of the Peg Solitaire logic: representing a board position and validating
whether a jump move is legal.
 
Rules: A valid move jumps a peg orthogonally or diagonally over an adjacent
peg into an empty hole exactly two positions away, in a straight line.
"""
 
 
class Position:
    """A single (row, col) location on the board."""
 
    def __init__(self, row, col):
        self.row = row
        self.col = col
 
    def __eq__(self, other):
        return isinstance(other, Position) and (self.row, self.col) == (other.row, other.col)
 
    def __hash__(self):
        return hash((self.row, self.col))
 
    def __repr__(self):
        return f"Position({self.row}, {self.col})"
 
 
def midpoint(start, end):
    """Return the Position halfway between start and end (the peg that
    would be jumped over), or None if start/end are not exactly two
    squares apart in a straight line (horizontal, vertical, or diagonal)."""
    row_diff = end.row - start.row
    col_diff = end.col - start.col
 
    # Must move exactly 2 in a straight line: horizontal, vertical, or diagonal.
    if abs(row_diff) == 2 and col_diff == 0:
        return Position(start.row + row_diff // 2, start.col)
    if abs(col_diff) == 2 and row_diff == 0:
        return Position(start.row, start.col + col_diff // 2)
    if abs(row_diff) == 2 and abs(col_diff) == 2:
        return Position(start.row + row_diff // 2, start.col + col_diff // 2)
    return None
 
 
def is_valid_move(board, start, end):
    """Given a board (dict mapping Position -> bool, True = peg present),
    return True if jumping from start to end is a legal Solitaire move."""
    if board.get(start) is not True:
        return False  # no peg at the start
    if board.get(end) is not False:
        return False  # destination must be an existing, empty hole
 
    mid = midpoint(start, end)
    if mid is None:
        return False  # not exactly two squares away in a straight line
 
    return board.get(mid) is True  # must be jumping over a peg
 