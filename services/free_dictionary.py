"""Free Dictionary API provider for the Words application."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

import requests
import streamlit as st


BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"
TIMEOUT_SECONDS = 10


@st.cache_data(show_spinner=False, ttl=3600)
def get_word(word: str) -> dict[str, Any] | None:
    """Return the first Free Dictionary API entry for *word*, if available."""
    normalized_word = word.strip().lower()
    if not normalized_word:
        return None

    try:
        response = requests.get(
            f"{BASE_URL}{quote(normalized_word, safe='')}",
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        entries = response.json()
    except (requests.RequestException, ValueError):
        return None

    return entries[0] if isinstance(entries, list) and entries else None


def _definitions(data: dict[str, Any]) -> list[dict[str, Any]]:
    definitions: list[dict[str, Any]] = []
    for meaning in data.get("meanings", []):
        part_of_speech = meaning.get("partOfSpeech", "")
        for item in meaning.get("definitions", []):
            definitions.append(
                {
                    "part_of_speech": part_of_speech,
                    "definition": item.get("definition", ""),
                    "example": item.get("example", ""),
                    "synonyms": item.get("synonyms", []),
                    "antonyms": item.get("antonyms", []),
                }
            )
    return definitions


def _related_words(data: dict[str, Any], relation: str) -> list[str]:
    values: set[str] = set()
    for meaning in data.get("meanings", []):
        values.update(meaning.get(relation, []))
        for definition in meaning.get("definitions", []):
            values.update(definition.get(relation, []))
    return sorted(value for value in values if isinstance(value, str) and value)


def _first_phonetic_value(data: dict[str, Any], key: str) -> str | None:
    for phonetic in data.get("phonetics", []):
        value = phonetic.get(key)
        if value:
            return value
    return data.get("phonetic") if key == "text" else None


def summarize(word: str) -> dict[str, Any] | None:
    """Return a UI-ready dictionary summary for *word*."""
    data = get_word(word)
    if not data:
        return None

    return {
        "word": data.get("word", word),
        "ipa": _first_phonetic_value(data, "text"),
        "audio": _first_phonetic_value(data, "audio"),
        "definitions": _definitions(data),
        "synonyms": _related_words(data, "synonyms"),
        "antonyms": _related_words(data, "antonyms"),
    }
