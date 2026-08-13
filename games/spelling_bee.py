from __future__ import annotations
from games.base_game import clean_word


def valid_bee_word(word: str, letters: str, center: str, minimum: int = 4) -> bool:
    word, letters, center = clean_word(word), set(clean_word(letters)), clean_word(center)
    return len(word) >= minimum and center in word and set(word).issubset(letters)


def is_pangram(word: str, letters: str) -> bool:
    return set(clean_word(letters)).issubset(set(clean_word(word)))


# Every word below is verified against valid_bee_word()/is_pangram() before
# shipping: 4+ letters, built only from `letters`, and containing `center`.
BEE_PUZZLES = [
    {
        "letters": "aelngru", "center": "a",
        "words": {"angle", "angel", "anger", "range", "learn", "large", "regular", "granular"},
    },
    {
        # Fixed: the previous version included "pencil" and "explain", which
        # both use letters outside this set and could never actually be
        # entered as valid answers.
        "letters": "eilnopx", "center": "e",
        "words": {"line", "pile", "exile", "pixel", "pixie", "expel", "nope", "lone", "opine", "linen"},
    },
    {
        "letters": "cehiknt", "center": "i",
        "words": {
            "kitchen", "think", "chick", "thick", "chic", "itch", "nick", "tick",
            "kick", "nice", "knit", "niche", "ethic", "hint", "chin", "niece", "ethnic",
        },
    },
    {
        "letters": "aelnpty", "center": "e",
        "words": {
            "penalty", "plate", "plane", "panel", "eaten", "late", "tale", "pale",
            "leap", "plea", "neat", "ante", "tape", "lean", "petal", "plenty", "neatly",
        },
    },
    {
        "letters": "achirot", "center": "a",
        "words": {
            "chariot", "actor", "chair", "attic", "char", "orca", "ratio",
            "trait", "carat", "chart", "cart", "arch", "hair", "iota",
        },
    },
    {
        "letters": "aeginrt", "center": "a",
        "words": {
            "granite", "tearing", "grain", "giant", "eating", "rating", "again",
            "grate", "great", "irate", "garnet", "attire",
        },
    },
]