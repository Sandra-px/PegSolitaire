"""Peg Solitaire game rules, independent of the GUI.
Reuses the Position and is_valid_move helpers from the original peg_move.py.
"""
from peg_move import Position, is_valid_move

class PegSolitaire:
    TYPES = ('English', 'Hexagon', 'Diamond')
    def __init__(self, size=7, board_type='English'):
        self.new_game(size, board_type)

    def new_game(self, size, board_type):
        if not isinstance(size, int) or isinstance(size, bool) or size < 5 or size % 2 == 0:
            raise ValueError('Board size must be an odd integer of at least 5.')
        if board_type not in self.TYPES:
            raise ValueError('Invalid board type.')
        self.size, self.board_type = size, board_type
        self.cells = self._shape(size, board_type)
        center = (size // 2, size // 2)
        self.pegs = self.cells - {center}

    @staticmethod
    def _shape(n, kind):
        m = n // 2
        if kind == 'English':
            arm = max(1, n // 3)
            return {(r,c) for r in range(n) for c in range(n) if abs(r-m) <= arm or abs(c-m) <= arm}
        if kind == 'Diamond':
            return {(r,c) for r in range(n) for c in range(n) if abs(r-m)+abs(c-m) <= m}
        # Axial hex grid represented in an n-by-n rhombus, with hexagonal mask.
        return {(r,c) for r in range(n) for c in range(n) if abs(r-c) <= m}

    def directions(self):
        if self.board_type == 'Hexagon':
            return ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1))
        return ((dr,dc) for dr in (-1,0,1) for dc in (-1,0,1) if (dr,dc) != (0,0))

    def valid_moves(self):
        moves=[]
        board = {Position(r,c): ((r,c) in self.pegs) for r,c in self.cells}
        for r,c in self.pegs:
            for dr,dc in self.directions():
                mid=(r+dr,c+dc); dst=(r+2*dr,c+2*dc)
                if is_valid_move(board, Position(r,c), Position(*dst)) and mid in self.pegs:
                    moves.append(((r,c),dst))
        return moves

    def make_move(self, source, destination):
        if (source,destination) not in self.valid_moves():
            return False
        mid=((source[0]+destination[0])//2,(source[1]+destination[1])//2)
        self.pegs.remove(source)
        self.pegs.remove(mid)
        self.pegs.add(destination)
        return True

    def is_game_over(self):
        return len(self.pegs) <= 1 or not self.valid_moves()

    def rating(self):
        if not self.is_game_over():
            return None
        return {1:'Outstanding',2:'Very Good',3:'Good'}.get(len(self.pegs),'Average')
