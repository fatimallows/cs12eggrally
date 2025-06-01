import json
from pathlib import Path

LEADERBOARD_FILE_SAVE = Path("leaderboard.json")
LEADERBOARD_FILE_LOAD = Path("egg_rally/leaderboard.json")


def load_leaderboard() -> list[int]:
    if LEADERBOARD_FILE_LOAD.exists():
        with open(LEADERBOARD_FILE_LOAD, "r") as f:
            arr: list[int] = json.load(f)
            return arr.copy()
    return []


def save_leaderboard(leaderboard: list[float | int]) -> None:
    with open(LEADERBOARD_FILE_SAVE, "w") as f:
        json.dump(leaderboard, f)
