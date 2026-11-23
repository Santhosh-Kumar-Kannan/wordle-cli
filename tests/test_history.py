"""pytest tests for GameHistory."""

import json
from pathlib import Path

from history import GameHistory


def make_history(tmp_path: Path, results: list[bool]) -> GameHistory:
    """Build a history from a list of win/loss booleans."""
    history = GameHistory(tmp_path / "history.json")
    for won in results:
        history.record_game(won, 4 if won else 6, "crane")
    return history


def test_creates_file_if_missing(tmp_path: Path) -> None:
    GameHistory(tmp_path / "history.json")
    assert (tmp_path / "history.json").exists()


def test_empty_history_stats(tmp_path: Path) -> None:
    history = make_history(tmp_path, [])
    assert history.total_games == 0
    assert history.win_percentage == 0.0
    assert history.current_streak == 0
    assert history.best_streak == 0


def test_totals_and_percentage(tmp_path: Path) -> None:
    history = make_history(tmp_path, [True, False, True, True])
    assert history.total_games == 4
    assert history.total_wins == 3
    assert history.win_percentage == 75.0


def test_streaks(tmp_path: Path) -> None:
    # W W W L W W  -> best streak 3, current streak 2
    history = make_history(tmp_path, [True, True, True, False, True, True])
    assert history.best_streak == 3
    assert history.current_streak == 2


def test_current_streak_zero_after_loss(tmp_path: Path) -> None:
    history = make_history(tmp_path, [True, True, False])
    assert history.current_streak == 0
    assert history.best_streak == 2


def test_persists_between_sessions(tmp_path: Path) -> None:
    make_history(tmp_path, [True, False])
    reloaded = GameHistory(tmp_path / "history.json")
    assert reloaded.total_games == 2


def test_corrupt_file_does_not_crash(tmp_path: Path) -> None:
    path = tmp_path / "history.json"
    path.write_text("{not valid json")
    history = GameHistory(path)
    assert history.total_games == 0
    # The next save overwrites the bad file with valid JSON.
    history.record_game(True, 3, "crane")
    assert len(json.loads(path.read_text())) == 1
