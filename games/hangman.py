from __future__ import annotations

from dataclasses import dataclass, field
from games.base_game import clean_word


@dataclass
class HangmanGame:
    word: str
    max_misses: int = 6
    guessed: set[str] = field(default_factory=set)
    misses: int = 0

    def __post_init__(self): self.word = clean_word(self.word)
    @property
    def masked_word(self): return " ".join(letter if letter in self.guessed else "_" for letter in self.word)
    @property
    def won(self): return bool(self.word) and set(self.word).issubset(self.guessed)
    @property
    def lost(self): return self.misses >= self.max_misses and not self.won
    @property
    def finished(self): return self.won or self.lost
    def guess(self, letter: str) -> dict:
        letter = clean_word(letter)
        if len(letter) != 1 or self.finished: return {"valid": False, "message": "Enter one unused letter."}
        if letter in self.guessed: return {"valid": False, "message": "You already tried that letter."}
        self.guessed.add(letter)
        correct = letter in self.word
        if not correct: self.misses += 1
        return {"valid": True, "correct": correct, "won": self.won, "lost": self.lost}
