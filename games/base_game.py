"""Shared, dependency-free game helpers for the Words app.

Word source strategy:
1. Try a live pool from Datamuse (services.datamuse.game_words) — no
   API key required, effectively unlimited variety when online.
2. Fall back to the hardcoded FALLBACK_WORDS below when offline, the
   API is slow/unavailable, or too few results come back.
"""
from __future__ import annotations

import random
import re

import streamlit as st

try:
    from services.datamuse import game_words as _live_game_words
except Exception:
    _live_game_words = None


FALLBACK_WORDS = {
    "general": [
        "language", "puzzle", "library", "planet", "journey", "curious", "discover",
        "rainbow", "whisper", "telescope", "adventure", "mystery", "harmony", "wonder",
        "treasure", "imagine", "wander", "sparkle", "gentle", "brave", "quiet", "bright",
        "shadow", "melody", "riddle", "compass", "lantern", "voyage", "horizon", "echo",
    ],
    "animal": [
        "elephant", "penguin", "butterfly", "dolphin", "leopard", "otter", "giraffe",
        "kangaroo", "octopus", "hedgehog", "flamingo", "squirrel", "peacock", "tortoise",
        "raccoon", "walrus", "cheetah", "gorilla", "jellyfish", "chameleon", "koala",
        "meerkat", "pelican", "buffalo", "falcon", "panther", "seahorse", "wombat",
    ],
    "science": [
        "gravity", "molecule", "electron", "volcano", "crystal", "genome", "asteroid",
        "chemical", "particle", "bacteria", "mineral", "organism", "reaction", "friction",
        "magnetic", "compound", "spectrum", "velocity", "membrane", "hormone", "isotope",
        "nucleus", "photon", "gene", "enzyme", "orbit", "climate", "fossil",
    ],
    "nature": [
        "forest", "meadow", "river", "thunder", "sunflower", "ocean", "mountain",
        "glacier", "canyon", "prairie", "blossom", "wetland", "boulder", "waterfall",
        "avalanche", "coral", "desert", "jungle", "tide", "breeze", "orchard", "valley",
        "reef", "marsh", "bloom", "drought", "moss", "cliff",
    ],
    "technology": [
        "computer", "network", "browser", "program", "robot", "digital", "software",
        "keyboard", "wireless", "database", "internet", "hardware", "download", "upload",
        "gadget", "circuit", "sensor", "server", "battery", "cursor", "firmware", "pixel",
        "printer", "monitor", "cable", "signal", "storage", "backup",
    ],
    "food": [
        "avocado", "cinnamon", "pancake", "strawberry", "noodle", "biscuit", "omelette",
        "sandwich", "pretzel", "broccoli", "pumpkin", "waffle", "spinach", "coconut",
        "mustard", "lentil", "walnut", "vinegar", "yogurt", "seasoning", "gingerbread",
        "asparagus", "artichoke", "cranberry", "chowder", "risotto", "papaya", "granola",
    ],
    "space": [
        "galaxy", "nebula", "comet", "meteor", "satellite", "rocket", "cosmos", "eclipse",
        "orbit", "shuttle", "constellation", "supernova", "spacecraft", "telescope",
        "asteroid", "moonlight", "starlight", "universe", "solstice", "astronaut",
        "aurora", "crater", "lunar", "stellar", "cosmic",
    ],
    "sports": [
        "athlete", "stadium", "referee", "victory", "champion", "marathon", "gymnast",
        "hurdles", "goalpost", "dribble", "sprinter", "tournament", "javelin", "paddle",
        "wrestle", "cyclist", "trophy", "defense", "offense", "rebound", "penalty",
        "backhand", "fairway", "swimmer", "rally", "pitcher", "striker",
    ],
}


def clean_word(value: str) -> str:
    return re.sub(r"[^a-z]", "", (value or "").lower())


def valid_word(value: str, minimum: int = 3, maximum: int = 14) -> bool:
    value = clean_word(value)
    return minimum <= len(value) <= maximum


def normalise_words(words):
    return list(dict.fromkeys(clean_word(word) for word in words if valid_word(word)))


def _fallback_pool(category: str, minimum: int, maximum: int) -> list[str]:
    words = FALLBACK_WORDS.get(category, FALLBACK_WORDS["general"])
    return [word for word in normalise_words(words) if valid_word(word, minimum, maximum)]


@st.cache_data(show_spinner=False, ttl=1800)
def _live_pool(category: str, minimum: int, maximum: int, limit: int = 60) -> list[str]:
    """Cached live word pool from Datamuse. Empty list if unavailable."""
    if not _live_game_words:
        return []
    try:
        words = _live_game_words(category=category, limit=limit)
    except Exception:
        return []
    return [word for word in normalise_words(words) if valid_word(word, minimum, maximum)]


def word_pool(category: str = "general", minimum: int = 4, maximum: int = 10, min_pool_size: int = 6) -> list[str]:
    """Best available pool of words for *category*: live Datamuse first,
    hardcoded fallback if the live pool is too small or unavailable."""
    live = _live_pool(category, minimum, maximum)
    if len(live) >= min_pool_size:
        return live
    fallback = _fallback_pool(category, minimum, maximum)
    combined = list(dict.fromkeys(live + fallback))
    return combined or FALLBACK_WORDS["general"]


def choose_word(category: str = "general", minimum: int = 4, maximum: int = 10, candidates=None) -> str:
    if candidates is not None:
        pool = [word for word in normalise_words(candidates) if valid_word(word, minimum, maximum)]
        return random.choice(pool or FALLBACK_WORDS["general"])
    return random.choice(word_pool(category, minimum, maximum))


def choose_words(category: str = "general", count: int = 6, minimum: int = 4, maximum: int = 10, random_category: bool = False) -> list[str]:
    """Pick *count* distinct words — used where a game needs several at once
    (Word Search, multi-word rounds), pulling from live-or-fallback pool."""
    if random_category:
        category = random.choice(list(FALLBACK_WORDS.keys()))
    pool = word_pool(category, minimum, maximum, min_pool_size=count)
    if len(pool) < count:
        pool = list(dict.fromkeys(pool + _fallback_pool("general", minimum, maximum)))
    return random.sample(pool, min(count, len(pool)))