"""Unified dictionary service used by the Streamlit pages."""

from __future__ import annotations

from typing import Any, Iterable

from services.datamuse import profile as datamuse_profile
from services.etymology import analyze as analyze_etymology
from services.free_dictionary import summarize as free_dictionary_summary
from services.wordnik import summarize as wordnik_summary


def _merge_lists(*lists: Iterable[str] | None) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for items in lists:
        for item in items or []:
            if item and item not in seen:
                seen.add(item)
                output.append(item)
    return output


def summarize(word: str) -> dict[str, Any]:
    """Combine available provider responses into one stable result shape."""
    result: dict[str, Any] = {
        "word": word,
        "ipa": None,
        "audio": None,
        "definitions": [],
        "examples": [],
        "synonyms": [],
        "antonyms": [],
        "related": [],
        "sounds_like": [],
        "rhymes": [],
        "triggers": [],
        "adjectives": [],
        "nouns": [],
        "etymology": None,
        "frequency": None,
        "syllables": None,
    }

    free_dictionary = free_dictionary_summary(word)
    if free_dictionary:
        result.update(
            {
                "word": free_dictionary.get("word", word),
                "ipa": free_dictionary.get("ipa"),
                "audio": free_dictionary.get("audio"),
                "definitions": free_dictionary.get("definitions", []),
                "synonyms": free_dictionary.get("synonyms", []),
                "antonyms": free_dictionary.get("antonyms", []),
            }
        )
        result["examples"] = [
            definition["example"]
            for definition in result["definitions"]
            if definition.get("example")
        ]

    datamuse = datamuse_profile(word)
    metadata = datamuse.get("metadata", {})
    result["related"] = datamuse.get("related", [])
    result["rhymes"] = datamuse.get("rhymes", [])
    result["triggers"] = datamuse.get("related", [])
    result["adjectives"] = datamuse.get("describing", [])
    result["nouns"] = datamuse.get("described_by", [])
    result["synonyms"] = _merge_lists(result["synonyms"], datamuse.get("synonyms"))
    result["antonyms"] = _merge_lists(result["antonyms"], datamuse.get("antonyms"))
    result["frequency"] = metadata.get("tags", [])
    result["syllables"] = metadata.get("numSyllables")

    wordnik = wordnik_summary(word)
    if wordnik:
        # Wordnik fills gaps rather than overriding a source that already answered.
        if not result["definitions"]:
            result["definitions"] = wordnik.get("definitions", [])
        result["examples"] = _merge_lists(result["examples"], wordnik.get("examples"))
        result["synonyms"] = _merge_lists(result["synonyms"], wordnik.get("synonyms"))
        result["antonyms"] = _merge_lists(result["antonyms"], wordnik.get("antonyms"))
        result["ipa"] = result["ipa"] or wordnik.get("ipa")
        result["audio"] = result["audio"] or wordnik.get("audio")

    etymology = analyze_etymology(word)
    result["etymology"] = etymology.get("history") or etymology.get("summary")
    return result