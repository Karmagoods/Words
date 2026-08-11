DIFFICULTY = {
    "Easy": {"word_length": (4, 6), "attempts": 8, "grid": 10},
    "Medium": {"word_length": (5, 8), "attempts": 6, "grid": 12},
    "Hard": {"word_length": (6, 11), "attempts": 5, "grid": 14},
}


def settings(level: str):
    return DIFFICULTY.get(level, DIFFICULTY["Easy"])
