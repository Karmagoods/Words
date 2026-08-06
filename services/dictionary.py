"""
==========================================================
Dictionary Service
----------------------------------------------------------
Uses the Free Dictionary API

https://dictionaryapi.dev/

Features
---------
✓ Definitions
✓ Parts of Speech
✓ Phonetics
✓ Audio
✓ Examples
✓ Synonyms
✓ Antonyms
==========================================================
"""

import requests
import streamlit as st

BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"


# ----------------------------------------------------------
# Fetch Word
# ----------------------------------------------------------

@st.cache_data(show_spinner=False)
def get_word(word: str):
    """
    Retrieve dictionary data for a word.

    Returns:
        dict or None
    """

    word = word.strip().lower()

    if not word:
        return None

    try:

        response = requests.get(
            BASE_URL + word,
            timeout=10
        )

        if response.status_code != 200:
            return None

        return response.json()[0]

    except Exception:

        return None


# ----------------------------------------------------------
# Word
# ----------------------------------------------------------

def get_word_name(data):

    if not data:
        return None

    return data.get("word")


# ----------------------------------------------------------
# Phonetics
# ----------------------------------------------------------

def get_phonetics(data):

    if not data:
        return []

    return data.get("phonetics", [])


# ----------------------------------------------------------
# Meanings
# ----------------------------------------------------------

def get_meanings(data):

    if not data:
        return []

    return data.get("meanings", [])


# ----------------------------------------------------------
# Definitions
# ----------------------------------------------------------

def get_definitions(data):

    definitions = []

    if not data:
        return definitions

    for meaning in data.get("meanings", []):

        pos = meaning.get("partOfSpeech", "")

        for d in meaning.get("definitions", []):

            definitions.append({

                "part_of_speech": pos,
                "definition": d.get("definition", ""),
                "example": d.get("example", ""),
                "synonyms": d.get("synonyms", []),
                "antonyms": d.get("antonyms", [])

            })

    return definitions


# ----------------------------------------------------------
# Synonyms
# ----------------------------------------------------------

def get_synonyms(data):

    synonyms = set()

    if not data:
        return []

    for meaning in data.get("meanings", []):

        synonyms.update(meaning.get("synonyms", []))

        for definition in meaning.get("definitions", []):

            synonyms.update(definition.get("synonyms", []))

    return sorted(list(synonyms))


# ----------------------------------------------------------
# Antonyms
# ----------------------------------------------------------

def get_antonyms(data):

    antonyms = set()

    if not data:
        return []

    for meaning in data.get("meanings", []):

        antonyms.update(meaning.get("antonyms", []))

        for definition in meaning.get("definitions", []):

            antonyms.update(definition.get("antonyms", []))

    return sorted(list(antonyms))


# ----------------------------------------------------------
# Audio
# ----------------------------------------------------------

def get_audio(data):

    if not data:
        return None

    for phonetic in data.get("phonetics", []):

        audio = phonetic.get("audio")

        if audio:
            return audio

    return None


# ----------------------------------------------------------
# IPA
# ----------------------------------------------------------

def get_ipa(data):

    if not data:
        return None

    for phonetic in data.get("phonetics", []):

        text = phonetic.get("text")

        if text:
            return text

    return None


# ----------------------------------------------------------
# Summary
# ----------------------------------------------------------

def summarize(word):

    data = get_word(word)

    if not data:

        return None

    return {

        "word": get_word_name(data),

        "ipa": get_ipa(data),

        "audio": get_audio(data),

        "definitions": get_definitions(data),

        "synonyms": get_synonyms(data),

        "antonyms": get_antonyms(data)

    }


# ----------------------------------------------------------
# Test
# ----------------------------------------------------------

if __name__ == "__main__":

    result = summarize("understanding")

    print(result)