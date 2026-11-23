"""Persistent game history, stored as JSON on disk."""

import json
from pathlib import Path
from typing import Any


class GameHistory:
    """A record of every completed game, saved to a JSON file.

    Each record is a dict like {"won": True, "attempts": 4, "word": "crane"}.
    The file is just a JSON list of those dicts, oldest game first.

    Attributes:
        path: Where the JSON file lives.
        games: The list of game records, oldest first.

    """

    def __init__(self, path: Path) -> None:
        """Remember the file path and load any existing history from it."""
        self.path = path
        self.games: list[dict[str, Any]] = []
        self.load()

    def load(self) -> None:
        """Read games from the file; create an empty file if it is missing."""
        if not self.path.exists():
            self.games = []
            self.save()  # "create the file if it does not exist"
            return
        try:
            with open(self.path, encoding="utf-8") as file:
                self.games = json.load(file)
        except json.JSONDecodeError:
            # A corrupt file should not crash the game. Start fresh; the next
            # save will overwrite the bad file.
            self.games = []

    def save(self) -> None:
        """Write all games to the file as JSON."""
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(self.games, file, indent=2)

    def record_game(self, won: bool, attempts: int, word: str) -> None:
        """Add a finished game to the history and save immediately."""
        self.games.append({"won": won, "attempts": attempts, "word": word})
        self.save()

    @property
    def total_games(self) -> int:
        """Number of games played."""
        return len(self.games)

    @property
    def total_wins(self) -> int:
        """Number of games won."""
        # Adding up True values: True counts as 1, False as 0.
        return sum(1 for game in self.games if game["won"])

    @property
    def win_percentage(self) -> float:
        """Percentage of games won (0.0 if no games have been played)."""
        if self.total_games == 0:
            return 0.0  # avoid dividing by zero
        return self.total_wins / self.total_games * 100

    @property
    def current_streak(self) -> int:
        """Consecutive wins ending at the most recent game.

        We walk backwards from the newest game and count wins until we hit
        the first loss. A loss most recently means the streak is 0.
        """
        streak = 0
        for game in reversed(self.games):
            if not game["won"]:
                break
            streak += 1
        return streak

    @property
    def best_streak(self) -> int:
        """The longest run of consecutive wins in the whole history.

        Walk forward through every game keeping a running streak. A win
        extends it; a loss resets it to 0. Remember the highest value seen.
        """
        best = 0
        running = 0
        for game in self.games:
            if game["won"]:
                running += 1
                best = max(best, running)
            else:
                running = 0
        return best
