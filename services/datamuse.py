"""
==========================================================
Datamuse Service
----------------------------------------------------------

https://api.datamuse.com/

Provides word relationship information.

Features
---------
✓ Similar Meaning
✓ Synonyms
✓ Antonyms
✓ Rhymes
✓ Near Rhymes
✓ Sounds Like
✓ Spelled Like
✓ Trigger Words
✓ Frequently Follows
✓ Frequently Precedes
✓ Adjectives
✓ Nouns
==========================================================
"""

import requests
import streamlit as st

BASE_URL = "https://api.datamuse.com/words"


# ----------------------------------------------------------
# Request Helper
# ----------------------------------------------------------

@st.cache_data(show_spinner=False)
def _query(params):
    """
    Execute a Datamuse query.
    """

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException:

        return []


# ----------------------------------------------------------
# Similar Meaning
# ----------------------------------------------------------

def get_similar(word, max_results=20):

    return _query({
        "ml": word,
        "max": max_results
    })


# ----------------------------------------------------------
# Synonyms
# ----------------------------------------------------------

def get_synonyms(word, max_results=20):

    return _query({
        "rel_syn": word,
        "max": max_results
    })


# ----------------------------------------------------------
# Antonyms
# ----------------------------------------------------------

def get_antonyms(word, max_results=20):

    return _query({
        "rel_ant": word,
        "max": max_results
    })


# ----------------------------------------------------------
# Rhymes
# ----------------------------------------------------------

def get_rhymes(word, max_results=20):

    return _query({
        "rel_rhy": word,
        "max": max_results
    })


# ----------------------------------------------------------
# Near Rhymes
# ----------------------------------------------------------

def get_near_rhymes(word, max_results=20):

    return _query({
        "rel_nry": word,
        "max": max_results
    })


# ----------------------------------------------------------
# Sounds Like
# ----------------------------------------------------------

def get_sounds_like(word, max_results=20):

    return _query({
        "sl": word,
        "max": max_results
    })


# ----------------------------------------------------------
# Spelled Like
# ----------------------------------------------------------

def get_spelled_like(word, max_results=20):

    return _query({
        "sp": word,
        "max": max_results
    })


# ----------------------------------------------------------
# Trigger Words
# ----------------------------------------------------------

def get_triggers(word, max_results=20):

    return _query({
        "rel_trg": word,
        "max": max_results
    })


# ----------------------------------------------------------
# Frequently Follows
# ----------------------------------------------------------

def get_after(word, max_results=20):

    return _query({
        "rel_bga": word,
        "max": max_results
    })


# ----------------------------------------------------------
# Frequently Precedes
# ----------------------------------------------------------

def get_before(word, max_results=20):

    return _query({
        "rel_bgb": word,
        "max": max_results
    })


# ----------------------------------------------------------
# Adjectives describing a noun
# ----------------------------------------------------------

def get_adjectives(word, max_results=20):

    return _query({
        "rel_jjb": word,
        "max": max_results
    })


# ----------------------------------------------------------
# Nouns described by adjective
# ----------------------------------------------------------

def get_nouns(word, max_results=20):

    return _query({
        "rel_jja": word,
        "max": max_results
    })


# ----------------------------------------------------------
# Extract words only
# ----------------------------------------------------------

def words_only(results):
    """
    Converts Datamuse results into
    a simple list of words.
    """

    return [item["word"] for item in results]


# ----------------------------------------------------------
# Complete Analysis
# ----------------------------------------------------------

def analyze(word):

    return {

        "similar": words_only(get_similar(word)),

        "synonyms": words_only(get_synonyms(word)),

        "antonyms": words_only(get_antonyms(word)),

        "rhymes": words_only(get_rhymes(word)),

        "near_rhymes": words_only(get_near_rhymes(word)),

        "sounds_like": words_only(get_sounds_like(word)),

        "spelled_like": words_only(get_spelled_like(word)),

        "triggers": words_only(get_triggers(word)),

        "before": words_only(get_before(word)),

        "after": words_only(get_after(word)),

        "adjectives": words_only(get_adjectives(word)),

        "nouns": words_only(get_nouns(word))

    }


# ----------------------------------------------------------
# Test
# ----------------------------------------------------------

if __name__ == "__main__":

    result = analyze("language")

    print(result)