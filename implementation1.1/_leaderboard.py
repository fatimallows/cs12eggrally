import json
from pathlib import Path

LEADERBOARD_FILE = Path("leaderboard.json")

def load_leaderboard() -> list[int]:
    if LEADERBOARD_FILE.exists():
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []

def save_leaderboard(leaderboard: list[int]) -> None:
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f)
