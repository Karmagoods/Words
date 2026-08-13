"""Wordnik API adapter.

Provides real definitions, examples, related words, pronunciations and
etymology data from the Wordnik v4 API. Configure WORDNIK_API_KEY in
.streamlit/secrets.toml to enable this provider. The app works fine
without a key or when a lookup fails — every function here degrades to
None/[] gracefully rather than raising.
"""

from __future__ import annotations

import re
from typing import Any

import requests
import streamlit as st

BASE_URL = "https://api.wordnik.com/v4"
TIMEOUT_SECONDS = 10


def _api_key() -> str | None:
    return st.secrets.get("WORDNIK_API_KEY", None)


def _get(path: str, word: str, **params: Any) -> Any:
    key = _api_key()
    if not key:
        return None

    params["api_key"] = key

    try:
        response = requests.get(
            f"{BASE_URL}/word.json/{word}/{path}",
            params=params,
            timeout=TIMEOUT_SECONDS,
        )
        if response.status_code != 200:
            return None
        return response.json()
    except (requests.RequestException, ValueError):
        return None


def _strip_tags(text: str) -> str:
    """Remove Wordnik's XML-style markup (<ety>, <xref>, <lang> etc.)."""
    return re.sub(r"<[^>]+>", "", text or "").strip()


@st.cache_data(show_spinner=False, ttl=3600)
def get_definitions(word: str, limit: int = 5) -> list[dict[str, Any]]:
    data = _get(
        "definitions", word,
        limit=limit, includeRelated="false", useCanonical="true",
    )
    if not data:
        return []

    definitions = []
    for entry in data:
        text = _strip_tags(entry.get("text", ""))
        if not text:
            continue
        definitions.append(
            {
                "part_of_speech": entry.get("partOfSpeech", ""),
                "definition": text,
                "example": "",
                "synonyms": [],
                "antonyms": [],
            }
        )
    return definitions


@st.cache_data(show_spinner=False, ttl=3600)
def get_examples(word: str, limit: int = 5) -> list[str]:
    data = _get("examples", word, limit=limit, useCanonical="true")
    if not data:
        return []

    examples = data.get("examples", [])
    return [
        _strip_tags(example.get("text", ""))
        for example in examples
        if example.get("text")
    ]


@st.cache_data(show_spinner=False, ttl=3600)
def get_related_words(word: str) -> dict[str, list[str]]:
    data = _get(
        "relatedWords", word,
        useCanonical="true", limitPerRelationshipType=10,
    )
    if not data:
        return {}

    related: dict[str, list[str]] = {}
    for entry in data:
        relation = entry.get("relationshipType")
        words = entry.get("words", [])
        if relation and words:
            related[relation] = words
    return related


@st.cache_data(show_spinner=False, ttl=3600)
def get_pronunciation(word: str) -> str | None:
    data = _get("pronunciations", word, useCanonical="true", limit=1)
    if not data:
        return None
    return data[0].get("raw")


@st.cache_data(show_spinner=False, ttl=3600)
def get_audio(word: str) -> str | None:
    data = _get("audio", word, useCanonical="true", limit=1)
    if not data:
        return None
    return data[0].get("fileUrl")


@st.cache_data(show_spinner=False, ttl=3600)
def get_etymologies(word: str) -> list[str]:
    """Return raw etymology strings for *word*, with markup stripped."""
    data = _get("etymologies", word, useCanonical="true")
    if not data:
        return []
    return [_strip_tags(entry) for entry in data if entry]


def summarize(word: str) -> dict[str, Any] | None:
    """Return a UI-ready Wordnik summary, or None if no key/no data."""
    if not _api_key():
        return None

    definitions = get_definitions(word)
    examples = get_examples(word)
    related = get_related_words(word)
    ipa = get_pronunciation(word)
    audio = get_audio(word)
    etymologies = get_etymologies(word)

    if not any([definitions, examples, related, ipa, audio, etymologies]):
        return None

    return {
        "word": word,
        "ipa": ipa,
        "audio": audio,
        "definitions": definitions,
        "examples": examples,
        "synonyms": related.get("synonym", []),
        "antonyms": related.get("antonym", []),
        "etymology": etymologies,
        "cognates": related.get("etymologically-related-term", []),
    }


if __name__ == "__main__":
    print(summarize("language"))