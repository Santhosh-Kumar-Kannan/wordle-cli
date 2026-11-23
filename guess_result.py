"""The GuessResult class: the outcome of a single guess."""

import messages
from letter_status import LetterStatus


class GuessResult:
    """The outcome of one guess: the guessed word plus a status per letter.

    Attributes:
        guess: The word that was guessed (lowercase).
        statuses: A list of LetterStatus, one per letter, same order as guess.
    """

    def __init__(self, guess: str, statuses: list[LetterStatus]) -> None:
        """Store the guess and its per-letter statuses."""
        self.guess = guess
        self.statuses = statuses

    @property
    def is_correct(self) -> bool:
        """True when every letter is in the correct position (a win)."""
        return all(status is LetterStatus.CORRECT for status in self.statuses)

    def __str__(self) -> str:
        """Render two lines: the letters, then a symbol under each letter.

        Example:
            S  P  E  E  D
            ✓  ✓  ~  ✗  ✗
        """
        sep = messages.CELL_SEPARATOR
        letters = sep.join(letter.upper() for letter in self.guess)
        symbols = sep.join(status.value for status in self.statuses)
        return f"{letters}\n{symbols}"
