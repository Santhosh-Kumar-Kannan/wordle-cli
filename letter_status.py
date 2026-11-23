"""The LetterStatus enum: the possible outcome for one letter of a guess."""

from enum import Enum

import messages


class LetterStatus(Enum):
    """The three possible outcomes for a single letter of a guess.

    An Enum is a fixed set of named values. It stops typos: LetterStatus.CORECT
    is an immediate error, whereas the string "corect" would silently be wrong.
    The value of each member is the symbol shown in the terminal.
    """

    CORRECT = messages.SYMBOL_CORRECT  # right letter, right position
    PRESENT = messages.SYMBOL_PRESENT  # right letter, wrong position
    ABSENT = messages.SYMBOL_ABSENT  # not in the word (or all copies used)
