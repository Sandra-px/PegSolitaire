"""Sprint 3
"""
import json
from game import PegSolitaire


class GameRecorder:
    """Records, saves, loads, and replays Peg Solitaire games."""

    def __init__(self, game):
        self.game = game
        self.board_size = game.size
        self.board_type = game.board_type
        self.initial_pegs = set(game.pegs)
        self.moves = []

    def record_move(self, start, end):
        """Record a move after it has succeeded."""
        self.moves.append({
            "start": list(start),
            "end": list(end)
        })

    def save_game(self, filename):
        """Save the game recording to a text file."""
        data = {
            "board_size": self.board_size,
            "board_type": self.board_type,
            "initial_pegs": [
                list(pos) for pos in sorted(self.initial_pegs)
            ],
            "moves": self.moves
        }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_game(filename):
        """Load a saved recording from a text file."""
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def replay_game(filename):
        """Reconstruct a saved game by replaying its moves."""
        data = GameRecorder.load_game(filename)

        game = PegSolitaire(
            data["board_size"],
            data["board_type"]
        )

        initial_pegs = {
            tuple(pos) for pos in data["initial_pegs"]
        }

        if not initial_pegs.issubset(game.cells):
            raise ValueError("Recording contains invalid peg positions.")

        game.pegs = initial_pegs

        for move in data["moves"]:
            start = tuple(move["start"])
            end = tuple(move["end"])

            if not game.make_move(start, end):
                raise ValueError(
                    f"Invalid recorded move: {start} -> {end}"
                )

        return game