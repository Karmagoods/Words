"""
==========================================================
Etymology Service
----------------------------------------------------------
Provides etymological information for the Words app.

Primary source:
    Wordnik

Fallback:
    Wiktionary

Reference source:
    Online Etymology Dictionary

The service is designed to fail gracefully. A missing API
key, unavailable source, malformed response, or parsing
problem should never break the application.

Wiktionary is accessed through the public MediaWiki API.
The service extracts the English Etymology section and
attempts to turn historical language/form information into
a structured timeline.

Etymonline is used as an external reference link rather
than scraped.
==========================================================
"""

from __future__ import annotations

import html
import re
from typing import Any

import requests
import streamlit as st

from services.wordnik import get_etymologies, get_related_words


# =========================================================
# CONSTANTS
# =========================================================

WIKTIONARY_API = "https://en.wiktionary.org/w/api.php"
WIKTIONARY_BASE_URL = "https://en.wiktionary.org/wiki/"

ETYMONLINE_BASE_URL = "https://www.etymonline.com/word/"

WORDNIK_BASE_URL = "https://www.wordnik.com/words/"


# =========================================================
# ETYMONLINE URL
# =========================================================

def _etymonline_url(word: str) -> str:
    """Build a direct Online Etymology Dictionary URL."""

    clean_word = word.strip().lower()

    return (
        ETYMONLINE_BASE_URL
        + requests.utils.quote(clean_word, safe="")
    )


# =========================================================
# LANGUAGE -> FAMILY MAP
# =========================================================

LANGUAGE_FAMILIES = {
    # Germanic
    "old english": "Germanic",
    "middle english": "Germanic",
    "early modern english": "Germanic",
    "modern english": "Germanic",
    "proto-germanic": "Germanic",
    "old frisian": "Germanic",
    "middle dutch": "Germanic",
    "old dutch": "Germanic",
    "old norse": "Germanic",
    "old icelandic": "Germanic",
    "gothic": "Germanic",
    "old high german": "Germanic",
    "middle high german": "Germanic",
    "old saxon": "Germanic",
    "german": "Germanic",
    "dutch": "Germanic",
    "english": "Germanic",

    # Italic / Romance
    "proto-italic": "Italic",
    "vulgar latin": "Italic",
    "classical latin": "Italic",
    "latin": "Italic",
    "old french": "Romance",
    "middle french": "Romance",
    "french": "Romance",
    "old occitan": "Romance",
    "occitan": "Romance",
    "old provençal": "Romance",
    "spanish": "Romance",
    "italian": "Romance",
    "portuguese": "Romance",
    "romanian": "Romance",
    "catalan": "Romance",

    # Hellenic
    "ancient greek": "Hellenic",
    "old greek": "Hellenic",
    "koine greek": "Hellenic",
    "classical greek": "Hellenic",
    "greek": "Hellenic",

    # Indo-Aryan
    "sanskrit": "Indo-Aryan",
    "vedic sanskrit": "Indo-Aryan",
    "hindi": "Indo-Aryan",
    "bengali": "Indo-Aryan",
    "urdu": "Indo-Aryan",
    "pali": "Indo-Aryan",
    "prakrit": "Indo-Aryan",

    # Celtic
    "old irish": "Celtic",
    "middle irish": "Celtic",
    "irish": "Celtic",
    "old welsh": "Celtic",
    "middle welsh": "Celtic",
    "welsh": "Celtic",
    "gaelic": "Celtic",
    "scottish gaelic": "Celtic",

    # Slavic
    "old church slavonic": "Slavic",
    "church slavonic": "Slavic",
    "old slavonic": "Slavic",
    "russian": "Slavic",
    "polish": "Slavic",
    "czech": "Slavic",
    "ukrainian": "Slavic",
    "serbo-croatian": "Slavic",

    # Semitic
    "arabic": "Semitic",
    "classical arabic": "Semitic",
    "hebrew": "Semitic",
    "biblical hebrew": "Semitic",
    "aramaic": "Semitic",
    "akkadian": "Semitic",

    # Iranian
    "persian": "Indo-Iranian",
    "old persian": "Indo-Iranian",
    "middle persian": "Indo-Iranian",
    "avestan": "Indo-Iranian",
    "kurdish": "Indo-Iranian",

    # Turkic
    "turkish": "Turkic",
    "old turkic": "Turkic",
    "ottoman turkish": "Turkic",

    # Other
    "japanese": "Japonic",
    "chinese": "Sino-Tibetan",
    "mandarin": "Sino-Tibetan",
    "korean": "Koreanic",

    # Proto-languages
    "proto-indo-european": "Indo-European",
    "proto-indo-iranian": "Indo-Iranian",
    "proto-balto-slavic": "Balto-Slavic",
    "proto-slavic": "Slavic",
    "proto-celtic": "Celtic",
    "proto-germanic": "Germanic",
    "proto-romance": "Romance",
}


# Longest language names first so that:
# "Middle English" wins before "English".
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


# =========================================================
# RESULT STRUCTURE
# =========================================================

def empty_result(word: str) -> dict[str, Any]:
    """Return a consistent result structure."""

    return {
        "word": word,
        "origin": None,

        # Current/root language information
        "language": None,
        "family": None,
        "origin_language": None,
        "origin_family": None,

        # Historical information
        "timeline": [],
        "history": None,
        "summary": None,

        # Relationships
        "cognates": [],
        "related_words": [],

        # Sources
        "source": None,
        "source_url": None,
        "etymonline_url": (
            _etymonline_url(word)
            if word
            else None
        ),

        # Additional metadata
        "wiktionary_found": False,
        "wiktionary_etymology": None,
    }


# =========================================================
# TEXT CLEANING
# =========================================================

def _clean_text(text: str) -> str:
    """
    Clean MediaWiki/plain-text fragments.

    Removes common wiki markup while preserving the actual
    historical information.
    """

    if not text:
        return ""

    text = html.unescape(text)

    # Remove HTML tags if any slipped through.
    text = re.sub(
        r"<[^>]+>",
        "",
        text,
    )

    # Remove templates such as {{lb|en|archaic}}.
    text = re.sub(
        r"\{\{.*?\}\}",
        "",
        text,
        flags=re.DOTALL,
    )

    # Convert wiki links:
    # [[word]] -> word
    # [[word|display]] -> display
    text = re.sub(
        r"\[\[([^|\]]+)\|([^\]]+)\]\]",
        r"\2",
        text,
    )

    text = re.sub(
        r"\[\[([^\]]+)\]\]",
        r"\1",
        text,
    )

    # Remove remaining emphasis markup.
    text = text.replace("'''", "")
    text = text.replace("''", "")

    # Remove excessive whitespace.
    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


# =========================================================
# LANGUAGE DETECTION
# =========================================================

def _detect_languages(text: str) -> list[str]:
    """
    Find distinct language names mentioned in text.

    Returned in order of appearance.
    """

    if not text:
        return []

    seen: list[str] = []

    for match in _LANGUAGE_PATTERN.finditer(text):
        name = match.group(1).lower()

        if name not in seen:
            seen.append(name)

    return seen


def _family_for_language(language: str | None) -> str | None:
    """Return the known language family."""

    if not language:
        return None

    return LANGUAGE_FAMILIES.get(
        language.strip().lower()
    )


# =========================================================
# HISTORICAL FORM EXTRACTION
# =========================================================

def _extract_historical_forms(
    text: str,
) -> list[dict[str, str | None]]:
    """
    Attempt to extract language + word pairs from
    common Wiktionary etymology phrasing.

    Examples this is designed to recognize:

        From Middle English felicité
        from Old French felicité
        from Latin fēlīcitās
        Proto-Germanic *...
        Old English ...
    """

    stages: list[dict[str, str | None]] = []

    if not text:
        return stages

    # -----------------------------------------------------
    # "from LANGUAGE WORD"
    # -----------------------------------------------------

    from_pattern = re.compile(
        r"\bfrom\s+"
        r"("
        + "|".join(
            sorted(
                LANGUAGE_FAMILIES,
                key=len,
                reverse=True,
            )
        )
        + r")"
        r"(?:\s+|:)"
        r"([^,.;()\n]+)",
        re.IGNORECASE,
    )

    for match in from_pattern.finditer(text):

        language = match.group(1).strip()
        historical_word = match.group(2).strip()

        # Avoid grabbing long chunks of prose.
        historical_word = historical_word.split(
            " from ",
            1,
        )[0]

        historical_word = historical_word.split(
            " ultimately ",
            1,
        )[0]

        historical_word = historical_word.strip(
            " -–—:"
        )

        if len(historical_word) > 80:
            continue

        stages.append(
            {
                "language": language.title(),
                "word": historical_word,
            }
        )

    # -----------------------------------------------------
    # "LANGUAGE WORD"
    #
    # Useful for forms such as:
    #
    # Latin fēlīcitās
    # Old English hēafod
    # -----------------------------------------------------

    language_pattern = re.compile(
        r"(?<!\w)"
        r"("
        + "|".join(
            sorted(
                LANGUAGE_FAMILIES,
                key=len,
                reverse=True,
            )
        )
        + r")"
        r"\s+"
        r"([A-Za-zÀ-žĀ-žŒœÆæÐðÞþĒēĪīŌōŪūĀāĔĕ]+"
        r"(?:[-'’][A-Za-zÀ-žĀ-žŒœÆæÐðÞþĒēĪīŌōŪūĀāĔĕ]+)*)",
        re.IGNORECASE,
    )

    for match in language_pattern.finditer(text):

        language = match.group(1).strip()
        historical_word = match.group(2).strip()

        candidate = {
            "language": language.title(),
            "word": historical_word,
        }

        if candidate not in stages:
            stages.append(candidate)

    return stages


# =========================================================
# TIMELINE
# =========================================================

def _build_timeline(
    stages: list[dict[str, str | None]],
    word: str,
) -> list[dict[str, str | None]]:
    """
    Build a historical timeline.

    The timeline contains actual extracted stages first,
    followed by the modern form.
    """

    timeline: list[dict[str, str | None]] = []

    seen: set[tuple[str, str]] = set()

    for stage in stages:

        language = (
            stage.get("language")
            or "Unknown"
        )

        historical_word = (
            stage.get("word")
            or ""
        )

        key = (
            language.lower(),
            historical_word.lower(),
        )

        if key in seen:
            continue

        seen.add(key)

        timeline.append(
            {
                "period": language,
                "language": language,
                "word": historical_word,
            }
        )

    # Modern form goes last.
    modern_key = (
        "english",
        word.lower(),
    )

    if modern_key not in seen:
        timeline.append(
            {
                "period": "Modern English",
                "language": "English",
                "word": word,
            }
        )

    return timeline


# =========================================================
# ETYMOLOGY SECTION EXTRACTION
# =========================================================

def _extract_english_etymology(
    extract: str,
) -> str | None:
    """
    Extract the English Etymology section from a Wiktionary
    plaintext page.

    Wiktionary plaintext commonly looks like:

        == English ==

        === Etymology ===
        From Middle English ...

        === Pronunciation ===

    We extract only the Etymology section.
    """

    if not extract:
        return None

    # Locate English section.
    english_match = re.search(
        r"(?im)^==\s*English\s*==\s*$",
        extract,
    )

    if not english_match:
        return None

    english_section = extract[
        english_match.end():
    ]

    # Stop at next top-level language section.
    next_language = re.search(
        r"(?m)^==\s*[^=].*?==\s*$",
        english_section,
    )

    if next_language:
        english_section = english_section[
            :next_language.start()
        ]

    # Find Etymology heading.
    etymology_match = re.search(
        r"(?im)^===+\s*Etymology(?:\s*\d+)?\s*===+\s*$",
        english_section,
    )

    if not etymology_match:
        return None

    etymology_section = english_section[
        etymology_match.end():
    ]

    # Stop at next subsection.
    next_subsection = re.search(
        r"(?m)^===+[^=].*?===+\s*$",
        etymology_section,
    )

    if next_subsection:
        etymology_section = etymology_section[
            :next_subsection.start()
        ]

    cleaned = _clean_text(
        etymology_section
    )

    if not cleaned:
        return None

    return cleaned


# =========================================================
# WIKTIONARY EXTRACT
# =========================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400,
)
def lookup_wiktionary(
    word: str,
) -> dict[str, Any] | None:
    """
    Retrieve the plaintext Wiktionary page through the
    MediaWiki Action API.

    We request the page extract rather than merely checking
    whether the page exists.
    """

    params = {
        "action": "query",
        "titles": word,
        "prop": "extracts",
        "explaintext": 1,
        "format": "json",
        "redirects": 1,
    }

    headers = {
        "User-Agent": (
            "KLH-Words/1.0 "
            "(https://klhinnovation-6eac7.web.app/)"
        ),
    }

    try:
        response = requests.get(
            WIKTIONARY_API,
            params=params,
            headers=headers,
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        pages = (
            data.get("query", {})
            .get("pages", {})
        )

        if not pages:
            return None

        page = next(
            iter(pages.values())
        )

        if page.get("missing") is not None:
            return None

        extract = page.get(
            "extract",
            "",
        )

        return {
            "pageid": page.get("pageid"),
            "title": page.get("title"),
            "extract": extract,
            "etymology": _extract_english_etymology(
                extract
            ),
        }

    except (
        requests.RequestException,
        ValueError,
        StopIteration,
    ):
        return None


# =========================================================
# WIKTIONARY STRUCTURED ANALYSIS
# =========================================================

def _parse_wiktionary_etymology(
    word: str,
    etymology: str,
) -> dict[str, Any]:
    """
    Turn a Wiktionary etymology paragraph into the common
    result structure used by the UI.
    """

    languages = _detect_languages(
        etymology
    )

    stages = _extract_historical_forms(
        etymology
    )

    # -----------------------------------------------------
    # Origin language
    # -----------------------------------------------------

    origin_language = None

    if stages:
        origin_language = (
            stages[-1]
            .get("language")
        )

    if languages and not origin_language:
        origin_language = languages[-1]

    # -----------------------------------------------------
    # Current language
    # -----------------------------------------------------

    current_language = "English"

    # -----------------------------------------------------
    # Families
    # -----------------------------------------------------

    origin_family = _family_for_language(
        origin_language
    )

    current_family = _family_for_language(
        current_language
    )

    # -----------------------------------------------------
    # Timeline
    # -----------------------------------------------------

    timeline = _build_timeline(
        stages,
        word,
    )

    return {
        "history": etymology,
        "summary": etymology,
        "language": current_language,
        "family": current_family,
        "origin_language": origin_language,
        "origin_family": origin_family,
        "timeline": timeline,
    }


# =========================================================
# WORDNIK RELATED WORDS
# =========================================================

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
            cognates
            or variants
        )

    except Exception:
        pass


# =========================================================
# WORDNIK ETYMOLOGY
# =========================================================

def _apply_wordnik(
    result: dict[str, Any],
    word: str,
    etymologies: list[str],
) -> None:
    """Apply Wordnik etymology information."""

    history = " ".join(
        item.strip()
        for item in etymologies
        if item and item.strip()
    )

    if not history:
        return

    result["history"] = history
    result["summary"] = etymologies[0]
    result["source"] = "Wordnik"

    result["source_url"] = (
        WORDNIK_BASE_URL
        + requests.utils.quote(
            word,
            safe="",
        )
    )

    languages = _detect_languages(
        history
    )

    if languages:
        result["origin_language"] = (
            languages[-1].title()
        )

        result["origin_family"] = (
            _family_for_language(
                languages[-1]
            )
        )

        result["language"] = "English"
        result["family"] = (
            _family_for_language(
                "English"
            )
        )

        stages = _extract_historical_forms(
            history
        )

        result["timeline"] = _build_timeline(
            stages,
            word,
        )

    else:
        result["language"] = "English"
        result["family"] = (
            _family_for_language(
                "English"
            )
        )

        result["timeline"] = [
            {
                "period": "Modern English",
                "language": "English",
                "word": word,
            }
        ]


# =========================================================
# MAIN ANALYSIS
# =========================================================

def analyze(
    word: str,
) -> dict[str, Any]:
    """
    Main entry point for the etymology UI.

    Source priority:

        1. Wordnik
        2. Wiktionary
        3. External Etymonline reference

    Unlike the previous version, Wiktionary is now actually
    parsed for its English Etymology section.
    """

    clean_word = word.strip()

    result = empty_result(
        clean_word
    )

    if not clean_word:
        result["summary"] = (
            "Please enter a word."
        )
        return result

    # =====================================================
    # 1. WORDNIK
    # =====================================================

    try:
        etymologies = get_etymologies(
            clean_word
        )
    except Exception:
        etymologies = []

    if etymologies:

        _apply_wordnik(
            result,
            clean_word,
            etymologies,
        )

        _add_related_words(
            result,
            clean_word,
        )

        return result

    # =====================================================
    # 2. WIKTIONARY
    # =====================================================

    raw = lookup_wiktionary(
        clean_word
    )

    if raw is not None:

        result["wiktionary_found"] = True
        result["source"] = "Wiktionary"

        result["source_url"] = (
            WIKTIONARY_BASE_URL
            + requests.utils.quote(
                clean_word,
                safe="",
            )
        )

        etymology = raw.get(
            "etymology"
        )

        if etymology:

            parsed = _parse_wiktionary_etymology(
                clean_word,
                etymology,
            )

            result.update(
                parsed
            )

            result["wiktionary_etymology"] = (
                etymology
            )

        else:

            result["summary"] = (
                "A Wiktionary entry exists for "
                "this word, but no English etymology "
                "section could be extracted."
            )

            result["language"] = "English"
            result["family"] = (
                _family_for_language(
                    "English"
                )
            )

            result["timeline"] = [
                {
                    "period": "Modern English",
                    "language": "English",
                    "word": clean_word,
                }
            ]

        # Wordnik related terms can still be useful even
        # when Wordnik has no etymology.
        _add_related_words(
            result,
            clean_word,
        )

        return result

    # =====================================================
    # 3. NO STRUCTURED DATA
    # =====================================================

    result["summary"] = (
        "No structured etymology data was found "
        "from the connected sources."
    )

    return result


# =========================================================
# LOCAL TEST
# =========================================================

if __name__ == "__main__":

    test_word = "felicity"

    result = analyze(
        test_word
    )

    print("=" * 60)
    print("ETYMOLOGY TEST")
    print("=" * 60)

    print(
        "WORD:",
        result["word"],
    )

    print(
        "SOURCE:",
        result["source"],
    )

    print(
        "LANGUAGE:",
        result["language"],
    )

    print(
        "FAMILY:",
        result["family"],
    )

    print(
        "ORIGIN LANGUAGE:",
        result["origin_language"],
    )

    print(
        "ORIGIN FAMILY:",
        result["origin_family"],
    )

    print(
        "ETYMONLINE:",
        result["etymonline_url"],
    )

    print()
    print("HISTORY:")
    print(
        result["history"]
    )

    print()
    print("TIMELINE:")

    for stage in result["timeline"]:
        print(
            " -",
            stage.get("language"),
            "->",
            stage.get("word"),
        )

    print()
    print("COGNATES:")
    print(
        result["cognates"]
    )

    print()
    print("RELATED:")
    print(
        result["related_words"]
    )

    print("=" * 60)