"""Entry point: run `python wordle.py` to play."""

import random
from pathlib import Path

import messages
from exceptions import WordleError
from game import MAX_GUESSES, WORD_LENGTH, Game, load_words
from history import GameHistory

# Path(__file__) is this file; .parent is its folder. Building paths this way
# means the game works no matter which directory you launch it from.
BASE_DIR = Path(__file__).parent
WORDS_FILE = BASE_DIR / "words.txt"
HISTORY_FILE = BASE_DIR / "history.json"


def play_round(game: Game) -> None:
    """Prompt for guesses until the game is won or lost."""
    while not game.is_over:
        print() # Adds a new line so the output won't look cramped
        print(game)
        guess = input(messages.GUESS_PROMPT)
        try:
            game.make_guess(guess)
        except WordleError as error:
            # The invalid guess was rejected before being recorded, so the
            # attempt count is unchanged. Just show why and loop again.
            print(messages.INVALID_GUESS.format(error=error))


def print_stats(history: GameHistory) -> None:
    """Print the player's overall statistics."""
    print(messages.STATS_HEADER)
    print(messages.STATS_GAMES.format(value=history.total_games))
    print(messages.STATS_WINS.format(value=history.total_wins))
    print(messages.STATS_WIN_PERCENTAGE.format(value=history.win_percentage))
    print(messages.STATS_CURRENT_STREAK.format(value=history.current_streak))
    print(messages.STATS_BEST_STREAK.format(value=history.best_streak))


def main() -> None:
    """Set up a game, play it, then record and show the results."""
    try:
        words = load_words(WORDS_FILE)
    except (OSError, WordleError) as error:
        print(messages.WORD_LIST_LOAD_FAILED.format(error=error))
        return

    secret = random.choice(words)
    game = Game(secret, words)
    history = GameHistory(HISTORY_FILE)

    print(messages.WELCOME.format(length=WORD_LENGTH))
    print(messages.LEGEND)

    try:
        play_round(game)
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C or Ctrl+D: quit without recording an unfinished game.
        print(messages.GAME_ABANDONED)
        return

    # Show the final board, then the outcome.
    print()
    print(game)
    if game.is_won:
        print(
            messages.WIN.format(attempts=game.attempts, max_guesses=MAX_GUESSES)
        )
    else:
        print(messages.LOSS.format(word=game.secret.upper()))

    history.record_game(game.is_won, game.attempts, game.secret)
    print_stats(history)


if __name__ == "__main__":
    main()
