"""Core Wordle logic: word loading, guess evaluation, and the Game class.

This module has no input() or print() calls for gameplay. It only holds the
*rules* of the game. The terminal interaction lives in wordle.py. Keeping the
two apart is what lets us test the rules easily with pytest.
"""

from pathlib import Path

import messages
from exceptions import (
    GameOverError,
    InvalidGuessLengthError,
    InvalidWordListError,
    WordNotInListError,
)
from guess_result import GuessResult
from letter_status import LetterStatus

# Constants: every other place in the project uses these names instead of the
# raw numbers 6 and 5. To make the game 7 guesses long, change one line.
MAX_GUESSES = 6
WORD_LENGTH = 5


# ---------------------------------------------------------------------------
# Word list loading
# ---------------------------------------------------------------------------


def load_words(path: Path) -> list[str]:
    """Read a word list file and return the words as a list.

    The file must have one word per line. Blank lines are skipped. Every word
    is lower-cased, and must be exactly WORD_LENGTH letters.

    Raises:
        InvalidWordListError: if any word has wrong length or has
            non-letter characters, or if the file contains no words at all.

    """
    words: list[str] = []
    with open(path, encoding="utf-8") as file:
        # enumerate gives us the line number too, which makes the error
        # message tell the user exactly where the problem is.
        for line_number, line in enumerate(file, start=1):
            word = line.strip().lower()
            if not word:
                continue  # ignore blank lines
            if len(word) != WORD_LENGTH or not word.isalpha():
                raise InvalidWordListError(
                    messages.INVALID_WORD_IN_FILE.format(
                        path=path,
                        line_number=line_number,
                        word=word,
                        length=WORD_LENGTH,
                    )
                )
            words.append(word)
    if not words:
        raise InvalidWordListError(messages.EMPTY_WORD_LIST.format(path=path))
    return words


# ---------------------------------------------------------------------------
# Guess evaluation
# ---------------------------------------------------------------------------


def evaluate_guess(secret: str, guess: str) -> GuessResult:
    """Compare a guess to the secret word and score every letter.

    The tricky part is duplicate letters. A letter in the secret can only
    "pay for" as many letters in the guess as it appears in the secret. So
    SPINE (one E) vs SPEED: only ONE of the two Es in the guess may be marked
    present; the other must be absent.

    We solve it with two passes:

    1. Mark exact-position matches CORRECT. Every letter of the secret that is
       NOT matched exactly goes into a pool of "unused" letters (a dict that
       counts how many of each letter remain).
    2. Go through the remaining guess letters left to right. If the letter is
       still in the pool, mark it PRESENT and use one copy up. Otherwise it is
       ABSENT.

    Doing the CORRECT pass first is what gives exact matches priority: a
    letter in the right spot always claims its copy before any PRESENT can.

    Args:
        secret: The hidden word.
        guess: The player's guess. Must be the same length as secret.

    Returns:
        A GuessResult with one status per letter.

    """
    secret = secret.lower()
    guess = guess.lower()

    # Start with everything ABSENT; passes below upgrade letters.
    statuses = [LetterStatus.ABSENT] * len(guess)

    # Pass 1: exact matches, and count the secret letters left over.
    unused: dict[str, int] = {}
    for i, secret_letter in enumerate(secret):
        if guess[i] == secret_letter:
            statuses[i] = LetterStatus.CORRECT
        else:
            # .get(letter, 0) returns 0 if we haven't seen this letter yet.
            unused[secret_letter] = unused.get(secret_letter, 0) + 1
    # Pass 2: for letters not already CORRECT, see if a copy is still unused.
    for i, guess_letter in enumerate(guess):
        if statuses[i] is LetterStatus.CORRECT:
            continue
        if unused.get(guess_letter, 0) > 0:
            statuses[i] = LetterStatus.PRESENT
            unused[guess_letter] -= 1

    return GuessResult(guess, statuses)


# ---------------------------------------------------------------------------
# Game
# ---------------------------------------------------------------------------


class Game:
    """One round of Wordle: a secret word and up to MAX_GUESSES attempts.

    Attributes:
        secret: The hidden word.
        words: The full list of allowed guesses.
        results: Every accepted guess so far, as GuessResult objects.

    """

    def __init__(self, secret: str, words: list[str]) -> None:
        """Create a game with a secret word and the list of valid words."""
        self.secret = secret.lower()
        self.words = words
        # A set makes "is this word allowed?" instant, however long the list.
        self._valid_words = {word.lower() for word in words}
        self.results: list[GuessResult] = []

    @property
    def attempts(self) -> int:
        """How many guesses have been made so far."""
        return len(self.results)

    @property
    def remaining_attempts(self) -> int:
        """How many guesses the player still has."""
        return MAX_GUESSES - self.attempts

    @property
    def is_won(self) -> bool:
        """True if the most recent guess was the secret word."""
        # `bool(self.results)` is False for an empty list, so we never try to
        # read results[-1] when no guesses exist yet.
        return bool(self.results) and self.results[-1].is_correct

    @property
    def is_over(self) -> bool:
        """True if the player has won or has used up all guesses."""
        return self.is_won or self.attempts >= MAX_GUESSES

    def make_guess(self, word: str) -> GuessResult:
        """Validate a guess, score it, record it, and return the result.

        Invalid guesses raise an exception and are NOT recorded, so they do
        not use up an attempt.

        Raises:
            GameOverError: the game has already been won or lost.
            InvalidGuessLengthError: the word is not WORD_LENGTH letters.
            WordNotInListError: the word is not in the word list.

        """
        if self.is_over:
            raise GameOverError(messages.GAME_ALREADY_OVER)

        word = word.strip().lower()

        if len(word) != WORD_LENGTH:
            raise InvalidGuessLengthError(
                messages.INVALID_GUESS_LENGTH.format(
                    length=WORD_LENGTH, actual=len(word)
                )
            )
        if word not in self._valid_words:
            raise WordNotInListError(messages.NOT_IN_LIST.format(word=word))

        result = evaluate_guess(self.secret, word)
        self.results.append(result)
        return result

    def __str__(self) -> str:
        """Render the whole board: past guesses, then attempts remaining."""
        blocks = [str(result) for result in self.results]
        # Empty rows for the guesses not yet used, to look like a real board.
        empty_row = messages.CELL_SEPARATOR.join([messages.EMPTY_CELL] * WORD_LENGTH)
        for _ in range(self.remaining_attempts):
            blocks.append(empty_row)
        board = messages.ROW_SEPARATOR.join(blocks)
        remaining = messages.ATTEMPTS_REMAINING.format(
            remaining=self.remaining_attempts
        )
        return f"{board}{messages.ROW_SEPARATOR}{remaining}"
