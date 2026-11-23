"""Every piece of user-facing text in one place.

Strings with {placeholders} are templates. Fill them in with .format():

    messages.NOT_IN_LIST.format(word="zzzzz")  ->  "'zzzzz' is not in the word list."

Keeping text here means a wording change (or a translation) touches only this
file, and the logic files stay free of hardcoded sentences.
"""

# --- Board symbols and layout ----------------------------------------------
SYMBOL_CORRECT = "✓"  # right letter, right position
SYMBOL_PRESENT = "~"  # right letter, wrong position
SYMBOL_ABSENT = "✗"  # letter not in the word (or all copies already used)
EMPTY_CELL = "_"  # an unused square on the board
CELL_SEPARATOR = "  "  # gap between squares on one row
ROW_SEPARATOR = "\n\n"  # gap between rows

ATTEMPTS_REMAINING = "Attempts remaining: {remaining}"

# --- Error messages (used when raising exceptions) -------------------------
INVALID_WORD_IN_FILE = (
    "{path} line {line_number}: {word!r} is not a {length}-letter word"
)
EMPTY_WORD_LIST = "{path} contains no words"
GAME_ALREADY_OVER = "The game is already over."
INVALID_GUESS_LENGTH = "Guess must be {length} letters, got {actual}."
NOT_IN_LIST = "'{word}' is not in the word list."

# --- Game loop text (wordle.py) --------------------------------------------
WELCOME = "Welcome to Wordle! Guess the {length}-letter word."
LEGEND = (
    f"{SYMBOL_CORRECT} = right spot   {SYMBOL_PRESENT} = wrong spot   "
    f"{SYMBOL_ABSENT} = not in word"
)
GUESS_PROMPT = "\nYour guess: "
INVALID_GUESS = "Invalid guess: {error}"
WORD_LIST_LOAD_FAILED = "Could not load word list: {error}"
GAME_ABANDONED = "\nGame abandoned."
WIN = "\nYou got it in {attempts}/{max_guesses}!"
LOSS = "\nThe word was {word}"

# --- Stats (wordle.py) -----------------------------------------------------
STATS_HEADER = "\n--- Your stats ---"
STATS_GAMES = "Games played:   {value}"
STATS_WINS = "Wins:           {value}"
STATS_WIN_PERCENTAGE = "Win percentage: {value:.0f}%"
STATS_CURRENT_STREAK = "Current streak: {value}"
STATS_BEST_STREAK = "Best streak:    {value}"
