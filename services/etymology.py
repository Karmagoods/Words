"""
==========================================================
Etymology Service
----------------------------------------------------------
Provides etymological information for the Words app.

Primary source: Wordnik (needs WORDNIK_API_KEY in secrets.toml).
Fallback: a lightweight note (no key configured / nothing found),
so the page never breaks, it just says less.
==========================================================
"""

from __future__ import annotations

import re
from typing import Any

import requests
import streamlit as st

from services.wordnik import get_etymologies, get_related_words

WIKTIONARY_API = "https://en.wiktionary.org/w/api.php"

# Rough language -> family map, matched against Wordnik's etymology text.
LANGUAGE_FAMILIES = {
    "old english": "Germanic",
    "middle english": "Germanic",
    "proto-germanic": "Germanic",
    "old frisian": "Germanic",
    "old norse": "Germanic",
    "gothic": "Germanic",
    "german": "Germanic",
    "dutch": "Germanic",
    "english": "Germanic",
    "vulgar latin": "Italic",
    "old french": "Romance",
    "french": "Romance",
    "latin": "Italic",
    "spanish": "Romance",
    "italian": "Romance",
    "portuguese": "Romance",
    "romanian": "Romance",
    "ancient greek": "Hellenic",
    "greek": "Hellenic",
    "sanskrit": "Indo-Aryan",
    "hindi": "Indo-Aryan",
    "arabic": "Semitic",
    "hebrew": "Semitic",
    "proto-indo-european": "Indo-European (root)",
}

# Longest names first so "old english" matches before bare "english".
_LANGUAGE_PATTERN = re.compile(
    r"\b(" + "|".join(sorted(LANGUAGE_FAMILIES, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)


def empty_result(word: str) -> dict[str, Any]:
    return {
        "word": word,
        "origin": None,
        "language": None,
        "family": None,
        "timeline": [],
        "history": None,
        "cognates": [],
        "related_words": [],
        "summary": None,
    }


def _detect_languages(text: str) -> list[str]:
    """Distinct language names mentioned in *text*, oldest-first as written."""
    seen: list[str] = []
    for match in _LANGUAGE_PATTERN.finditer(text):
        name = match.group(1).lower()
        if name not in seen:
            seen.append(name)
    return seen


def _build_timeline(languages: list[str], word: str) -> list[dict[str, str]]:
    timeline = [
        {"period": language.title(), "language": language.title(), "word": None}
        for language in languages
    ]
    timeline.append({"period": "Modern", "language": "English", "word": word})
    return timeline


@st.cache_data(show_spinner=False)
def lookup_wiktionary(word: str):
    """Check whether a Wiktionary page exists, as a last-resort fallback."""
    params = {"action": "parse", "page": word, "prop": "text", "format": "json"}
    try:
        response = requests.get(WIKTIONARY_API, params=params, timeout=15)
        if response.status_code != 200:
            return None
        return response.json()
    except Exception:
        return None


def analyze(word: str) -> dict[str, Any]:
    """Main entry point — the only function the UI should call.

    Prefers real Wordnik etymology data. Falls back to a short,
    honest note if no key is configured or nothing is found.
    """
    result = empty_result(word)

    etymologies = get_etymologies(word)

    if etymologies:
        history = " ".join(etymologies)
        result["history"] = history
        result["summary"] = etymologies[0]

        languages = _detect_languages(history)
        if languages:
            result["language"] = languages[0].title()
            result["family"] = LANGUAGE_FAMILIES.get(languages[0])
            result["timeline"] = _build_timeline(languages, word)
        else:
            result["timeline"] = [{"period": "Modern", "language": "English", "word": word}]

        related = get_related_words(word)
        cognates = related.get("etymologically-related-term", [])
        result["cognates"] = cognates
        result["related_words"] = cognates or related.get("variant", [])

        return result

    # No Wordnik key configured, or nothing found for this specific word.
    raw = lookup_wiktionary(word)
    if raw is not None:
        result["summary"] = (
            "No structured etymology was found for this word from Wordnik. "
            "A Wiktionary page exists for it if you want to check manually."
        )
    else:
        result["summary"] = "No etymology data is available for this word right now."

    result["timeline"] = [{"period": "Modern", "language": "English", "word": word}]
    return result


if __name__ == "__main__":
    print(analyze("language"))