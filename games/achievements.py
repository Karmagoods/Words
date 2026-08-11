ACHIEVEMENTS = {
    "first_win": "First victory",
    "wordsmith": "Solve five games",
    "no_hints": "Win without a hint",
    "daily": "Complete a daily challenge",
}


def unlocked(stats: dict) -> list[str]:
    result = []
    if stats.get("wins", 0) >= 1: result.append("first_win")
    if stats.get("wins", 0) >= 5: result.append("wordsmith")
    if stats.get("no_hint_wins", 0) >= 1: result.append("no_hints")
    if stats.get("daily_wins", 0) >= 1: result.append("daily")
    return result
