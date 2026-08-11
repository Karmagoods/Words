from __future__ import annotations
import random
from games.base_game import clean_word


def scramble(word: str) -> str:
    word = clean_word(word)
    if len(set(word)) < 2: return word
    letters = list(word)
    for _ in range(8):
        random.shuffle(letters)
        candidate = "".join(letters)
        if candidate != word: return candidate
    return "".join(reversed(word))


def is_correct(answer: str, word: str) -> bool:
    return clean_word(answer) == clean_word(word)
