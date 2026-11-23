"""Custom exceptions raised on purpose by the Wordle project.

We define our own exception classes so callers can catch exactly the problem
they care about. They all inherit from WordleError, so `except WordleError`
catches any of them at once.
"""


class WordleError(Exception):
    """Base class for every error this project raises on purpose."""


class InvalidWordListError(WordleError):
    """The word list file contains a line that is not a valid word."""


class InvalidGuessLengthError(WordleError):
    """A guess did not have exactly WORD_LENGTH letters."""


class WordNotInListError(WordleError):
    """A guess was the right length but is not in the word list."""


class GameOverError(WordleError):
    """A guess was attempted after the game had already finished."""
