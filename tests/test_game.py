"""pytest tests for the Wordle game logic."""

import pytest

from exceptions import (
    GameOverError,
    InvalidGuessLengthError,
    InvalidWordListError,
    WordNotInListError,
)
from game import MAX_GUESSES, Game, evaluate_guess, load_words
from letter_status import LetterStatus

C = LetterStatus.CORRECT
P = LetterStatus.PRESENT
A = LetterStatus.ABSENT

WORDS = ["spine", "speed", "crane", "apple", "brave", "stone"]


# --- evaluate_guess --------------------------------------------------------


def test_evaluate_fully_correct() -> None:
    result = evaluate_guess("crane", "crane")
    assert result.statuses == [C, C, C, C, C]
    assert result.is_correct


def test_evaluate_mixed_letters() -> None:
    # secret CRANE, guess CARTS: C correct, A present, R present, T/S absent
    result = evaluate_guess("crane", "carts")
    assert result.statuses == [C, P, P, A, A]
    assert not result.is_correct


def test_evaluate_duplicate_letters_in_guess() -> None:
    # SPINE has one E. SPEED has two: first is present, second absent.
    result = evaluate_guess("spine", "speed")
    assert result.statuses == [C, C, P, A, A]


def test_evaluate_correct_takes_priority_over_present() -> None:
    # SPINE has one E. In EERIE the LAST E is in the right spot, so it claims
    # that single E. The earlier Es must therefore be absent, not present.
    result = evaluate_guess("spine", "eerie")
    assert result.statuses == [A, A, A, P, C]


def test_str_output_format() -> None:
    result = evaluate_guess("spine", "speed")
    assert str(result) == "S  P  E  E  D\n✓  ✓  ~  ✗  ✗"


# --- Game ------------------------------------------------------------------


def test_make_guess_rejects_word_not_in_list() -> None:
    game = Game("crane", WORDS)
    with pytest.raises(WordNotInListError):
        game.make_guess("zzzzz")


def test_make_guess_rejects_wrong_length() -> None:
    game = Game("crane", WORDS)
    with pytest.raises(InvalidGuessLengthError):
        game.make_guess("cat")


def test_invalid_guess_does_not_use_an_attempt() -> None:
    game = Game("crane", WORDS)
    with pytest.raises(WordNotInListError):
        game.make_guess("zzzzz")
    assert game.attempts == 0


def test_is_won_after_correct_guess() -> None:
    game = Game("crane", WORDS)
    assert not game.is_won
    game.make_guess("crane")
    assert game.is_won
    assert game.is_over


def test_is_over_after_max_failed_guesses() -> None:
    game = Game("crane", WORDS)
    for _ in range(MAX_GUESSES):
        assert not game.is_over
        game.make_guess("apple")
    assert game.is_over
    assert not game.is_won


def test_make_guess_after_game_over_raises() -> None:
    game = Game("crane", WORDS)
    game.make_guess("crane")
    with pytest.raises(GameOverError):
        game.make_guess("apple")


def test_guess_is_case_insensitive() -> None:
    game = Game("crane", WORDS)
    game.make_guess("CRANE")
    assert game.is_won


# --- load_words ------------------------------------------------------------


def test_load_words_rejects_bad_length(tmp_path) -> None:
    bad_file = tmp_path / "words.txt"
    bad_file.write_text("apple\ncat\n")
    with pytest.raises(InvalidWordListError):
        load_words(bad_file)


def test_load_words_reads_valid_file(tmp_path) -> None:
    good_file = tmp_path / "words.txt"
    good_file.write_text("apple\nCRANE\n\n")
    assert load_words(good_file) == ["apple", "crane"]
