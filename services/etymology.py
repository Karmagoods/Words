
"""
==========================================================
Etymology Service
----------------------------------------------------------
Provides etymological information for the Words app.

Primary source: Wordnik
Fallback: Wiktionary
Reference source: Online Etymology Dictionary

The service is designed so that a missing API key or a
failed lookup does not break the application.

Etymonline is used as a reference link rather than scraped,
so the app does not depend on an unofficial scraping API.
==========================================================
"""

from __future__ import annotations

import re
from typing import Any

import requests
import streamlit as st

from services.wordnik import get_etymologies, get_related_words


# ---------------------------------------------------------
# WIKTIONARY
# ---------------------------------------------------------

WIKTIONARY_API = "https://en.wiktionary.org/w/api.php"
WIKTIONARY_BASE_URL = "https://en.wiktionary.org/wiki/"


# ---------------------------------------------------------
# ETYMONLINE
# ---------------------------------------------------------

ETYMONLINE_BASE_URL = "https://www.etymonline.com/word/"


def _etymonline_url(word: str) -> str:
    """
    Build a direct Online Etymology Dictionary URL.

    Etymonline normally uses the word itself in the URL.
    """
    clean_word = word.strip().lower()

    return (
        ETYMONLINE_BASE_URL
        + requests.utils.quote(
            clean_word,
            safe="",
        )
    )


# ---------------------------------------------------------
# LANGUAGE -> FAMILY MAP
# ---------------------------------------------------------

LANGUAGE_FAMILIES = {
    # Germanic
    "old english": "Germanic",
    "middle english": "Germanic",
    "proto-germanic": "Germanic",
    "old frisian": "Germanic",
    "old norse": "Germanic",
    "gothic": "Germanic",
    "old high german": "Germanic",
    "middle high german": "Germanic",
    "german": "Germanic",
    "dutch": "Germanic",
    "english": "Germanic",

    # Italic / Romance
    "vulgar latin": "Italic",
    "latin": "Italic",
    "old french": "Romance",
    "middle french": "Romance",
    "french": "Romance",
    "spanish": "Romance",
    "italian": "Romance",
    "portuguese": "Romance",
    "romanian": "Romance",

    # Hellenic
    "ancient greek": "Hellenic",
    "old greek": "Hellenic",
    "greek": "Hellenic",

    # Indo-Aryan
    "sanskrit": "Indo-Aryan",
    "hindi": "Indo-Aryan",
    "bengali": "Indo-Aryan",
    "urdu": "Indo-Aryan",

    # Celtic
    "old irish": "Celtic",
    "irish": "Celtic",
    "welsh": "Celtic",
    "gaelic": "Celtic",

    # Slavic
    "old church slavonic": "Slavic",
    "church slavonic": "Slavic",
    "russian": "Slavic",
    "polish": "Slavic",
    "czech": "Slavic",

    # Semitic
    "arabic": "Semitic",
    "hebrew": "Semitic",
    "aramaic": "Semitic",

    # Turkic / Iranian
    "turkish": "Turkic",
    "persian": "Indo-Iranian",
    "old persian": "Indo-Iranian",

    # Proto-languages
    "proto-indo-european": "Indo-European",
    "proto-indo-iranian": "Indo-Iranian",
}


# Longest names first.
_LANGUAGE_PATTERN = re.compile(
    r"\b("
    + "|".join(
        sorted(
            LANGUAGE_FAMILIES,
            key=len,
            reverse=True,
        )
    )
    + r")\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------
# RESULT STRUCTURE
# ---------------------------------------------------------

def empty_result(word: str) -> dict[str, Any]:
    """Return a consistent result structure."""

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
        "source": None,
        "source_url": None,
        "etymonline_url": _etymonline_url(word) if word else None,
    }


# ---------------------------------------------------------
# LANGUAGE DETECTION
# ---------------------------------------------------------

def _detect_languages(text: str) -> list[str]:
    """
    Find distinct language names mentioned in etymology text.

    Languages are returned in the order they appear.
    """

    seen: list[str] = []

    for match in _LANGUAGE_PATTERN.finditer(text):
        name = match.group(1).lower()

        if name not in seen:
            seen.append(name)

    return seen


# ---------------------------------------------------------
# TIMELINE
# ---------------------------------------------------------

def _build_timeline(
    languages: list[str],
    word: str,
) -> list[dict[str, str | None]]:
    """Build a simple historical language timeline."""

    timeline: list[dict[str, str | None]] = []

    for language in languages:
        timeline.append(
            {
                "period": language.title(),
                "language": language.title(),
                "word": None,
            }
        )

    timeline.append(
        {
            "period": "Modern",
            "language": "English",
            "word": word,
        }
    )

    return timeline


# ---------------------------------------------------------
# WIKTIONARY LOOKUP
# ---------------------------------------------------------

@st.cache_data(show_spinner=False, ttl=86400)
def lookup_wiktionary(
    word: str,
) -> dict[str, Any] | None:
    """
    Check whether a Wiktionary page exists.

    This is currently a fallback indicator rather than a
    complete Wiktionary etymology parser.
    """

    params = {
        "action": "parse",
        "page": word,
        "prop": "text",
        "format": "json",
    }

    headers = {
        "User-Agent": "KLH-Words/1.0",
    }

    try:
        response = requests.get(
            WIKTIONARY_API,
            params=params,
            headers=headers,
            timeout=15,
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if "error" in data:
            return None

        return data

    except (
        requests.RequestException,
        ValueError,
    ):
        return None


# ---------------------------------------------------------
# WORDNIK RELATED WORDS
# ---------------------------------------------------------

def _add_related_words(
    result: dict[str, Any],
    word: str,
) -> None:
    """
    Add Wordnik related terms.

    Failure here never breaks the etymology result.
    """

    try:
        related = get_related_words(word)

        if not related:
            return

        cognates = related.get(
            "etymologically-related-term",
            [],
        )

        variants = related.get(
            "variant",
            [],
        )

        result["cognates"] = cognates

        result["related_words"] = (
            cognates or variants
        )

    except Exception:
        pass


# ---------------------------------------------------------
# MAIN ANALYSIS
# ---------------------------------------------------------

def analyze(word: str) -> dict[str, Any]:
    """
    Main entry point for the etymology UI.

    Source priority:

        1. Wordnik
        2. Wiktionary
        3. Etymonline reference link
        4. No data

    Etymonline is always supplied as an external reference
    link when a word has been entered.
    """

    clean_word = word.strip()

    result = empty_result(clean_word)

    if not clean_word:
        result["summary"] = "Please enter a word."
        return result

    # -----------------------------------------------------
    # 1. WORDNIK
    # -----------------------------------------------------

    try:
        etymologies = get_etymologies(clean_word)
    except Exception:
        etymologies = []

    if etymologies:
        history = " ".join(etymologies)

        result["history"] = history
        result["summary"] = etymologies[0]
        result["source"] = "Wordnik"
        result["source_url"] = (
            "https://www.wordnik.com/words/"
            + requests.utils.quote(
                clean_word,
                safe="",
            )
        )

        languages = _detect_languages(history)

        if languages:
            result["language"] = languages[0].title()

            result["family"] = LANGUAGE_FAMILIES.get(
                languages[0]
            )

            result["timeline"] = _build_timeline(
                languages,
                clean_word,
            )

        else:
            result["timeline"] = [
                {
                    "period": "Modern",
                    "language": "English",
                    "word": clean_word,
                }
            ]

        _add_related_words(
            result,
            clean_word,
        )

        return result

    # -----------------------------------------------------
    # 2. WIKTIONARY FALLBACK
    # -----------------------------------------------------

    raw = lookup_wiktionary(clean_word)

    if raw is not None:
        result["summary"] = (
            "No structured etymology was found "
            "from Wordnik. A Wiktionary entry exists "
            "for this word and can be checked manually."
        )

        result["source"] = "Wiktionary"

        result["source_url"] = (
            WIKTIONARY_BASE_URL
            + requests.utils.quote(
                clean_word,
                safe="",
            )
        )

    # -----------------------------------------------------
    # 3. NO API DATA
    # -----------------------------------------------------

    else:
        result["summary"] = (
            "No etymology data is available from "
            "the connected sources right now."
        )

    result["timeline"] = [
        {
            "period": "Modern",
            "language": "English",
            "word": clean_word,
        }
    ]

    return result


# ---------------------------------------------------------
# LOCAL TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    result = analyze("language")

    print("WORD:", result["word"])
    print("SOURCE:", result["source"])
    print("LANGUAGE:", result["language"])
    print("FAMILY:", result["family"])
    print("ETYMONLINE:", result["etymonline_url"])
    print()
    print("SUMMARY:")
    print(result["summary"])
