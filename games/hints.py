from __future__ import annotations


def reveal_letter(word: str, guessed: set[str]) -> str | None:
    return next((letter for letter in word if letter not in guessed), None)


def word_hint(word: str) -> str:
    return f"It has {len(word)} letters and begins with '{word[0].upper()}'."
