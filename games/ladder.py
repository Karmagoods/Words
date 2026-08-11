from __future__ import annotations
from games.base_game import clean_word


def one_letter_apart(first: str, second: str) -> bool:
    first, second = clean_word(first), clean_word(second)
    return len(first) == len(second) and sum(a != b for a, b in zip(first, second)) == 1


def validate_step(previous: str, candidate: str, allowed_words: set[str]) -> tuple[bool, str]:
    candidate = clean_word(candidate)
    if candidate not in allowed_words: return False, "That word is not in this puzzle's word list."
    if not one_letter_apart(previous, candidate): return False, "Change exactly one letter each step."
    return True, "Good step!"


LADDERS = [("cold", "warm", {"cold", "cord", "card", "ward", "warm", "word", "worm", "form", "farm"}), ("lead", "gold", {"lead", "load", "goad", "gold", "loan", "lean", "bean", "bold"})]
