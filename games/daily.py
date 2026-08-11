from __future__ import annotations
from datetime import date
from games.base_game import FALLBACK_WORDS


def daily_word(on_date: date | None = None) -> str:
    on_date = on_date or date.today()
    words = sum(FALLBACK_WORDS.values(), [])
    return words[on_date.toordinal() % len(words)]


def challenge(on_date: date | None = None) -> dict:
    on_date = on_date or date.today()
    return {"date": on_date.isoformat(), "word": daily_word(on_date), "hint": "Solve the daily word in any of the game modes."}
