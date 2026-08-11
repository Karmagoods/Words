"""Shared, dependency-free game helpers for the Words app."""
from __future__ import annotations

import random
import re

FALLBACK_WORDS = {
    "general": ["language", "puzzle", "library", "planet", "journey", "curious", "discover", "rainbow", "whisper", "telescope"],
    "animal": ["elephant", "penguin", "butterfly", "dolphin", "leopard", "otter"],
    "science": ["gravity", "molecule", "electron", "volcano", "crystal", "genome"],
    "nature": ["forest", "meadow", "river", "thunder", "sunflower", "ocean"],
    "technology": ["computer", "network", "browser", "program", "robot", "digital"],
    "food": ["avocado", "cinnamon", "pancake", "strawberry", "noodle", "biscuit"],
}


def clean_word(value: str) -> str:
    return re.sub(r"[^a-z]", "", (value or "").lower())


def valid_word(value: str, minimum: int = 3, maximum: int = 14) -> bool:
    value = clean_word(value)
    return minimum <= len(value) <= maximum


def choose_word(category: str = "general", minimum: int = 4, maximum: int = 10, candidates=None) -> str:
    words = [clean_word(word) for word in (candidates or FALLBACK_WORDS.get(category, FALLBACK_WORDS["general"]))]
    words = [word for word in words if valid_word(word, minimum, maximum)]
    return random.choice(words or FALLBACK_WORDS["general"])


def normalise_words(words):
    return list(dict.fromkeys(clean_word(word) for word in words if valid_word(word)))
