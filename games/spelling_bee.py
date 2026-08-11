from __future__ import annotations
from games.base_game import clean_word


def valid_bee_word(word: str, letters: str, center: str, minimum: int = 4) -> bool:
    word, letters, center = clean_word(word), set(clean_word(letters)), clean_word(center)
    return len(word) >= minimum and center in word and set(word).issubset(letters)


def is_pangram(word: str, letters: str) -> bool:
    return set(clean_word(letters)).issubset(set(clean_word(word)))


BEE_PUZZLES = [{"letters": "aelngru", "center": "a", "words": {"angle", "angel", "anger", "range", "learn", "large", "regular", "granular"}}, {"letters": "eilnopx", "center": "e", "words": {"line", "pile", "pencil", "exile", "pixel", "explain"}}]
