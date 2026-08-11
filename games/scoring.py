"""Small, transparent scoring rules shared by all games."""

DIFFICULTY_MULTIPLIER = {"Easy": 1.0, "Medium": 1.5, "Hard": 2.0}


def score(base: int, difficulty: str = "Easy", hints_used: int = 0, bonus: int = 0) -> int:
    return max(0, round((base + bonus) * DIFFICULTY_MULTIPLIER.get(difficulty, 1.0)) - hints_used * 5)
