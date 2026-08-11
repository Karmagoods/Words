"""
==========================================================
Datamuse Service
----------------------------------------------------------

Wrapper around the Datamuse Word API.

Documentation:
https://www.datamuse.com/api/

Current:
✓ No API key required

Future:
✓ API key support ready (Jan 2027)

Features:
✓ Synonyms
✓ Antonyms
✓ Related words
✓ Rhymes
✓ Homophones
✓ Word games
✓ Autocomplete
✓ Word relationships
✓ Word metadata
✓ Crossword helpers
✓ Hangman helpers

==========================================================
"""

from typing import List, Dict
import requests
import streamlit as st


BASE_URL = "https://api.datamuse.com"

TIMEOUT = 6


# ==========================================================
# API KEY READY
# ==========================================================

def get_api_key():

    try:
        return st.secrets.get("DATAMUSE_API_KEY")

    except Exception:
        return None


# ==========================================================
# INTERNAL REQUEST
# ==========================================================

@st.cache_data(show_spinner=False)
def _query(params: Dict) -> List[Dict]:
    """
    Execute Datamuse /words query.
    """

    try:

        api_key = get_api_key()

        if api_key:
            params["key"] = api_key


        response = requests.get(
            f"{BASE_URL}/words",
            params=params,
            timeout=TIMEOUT
        )


        response.raise_for_status()

        return response.json()


    except Exception:

        return []


# ==========================================================
# AUTOCOMPLETE
# ==========================================================

@st.cache_data(show_spinner=False)
def autocomplete(
        prefix: str,
        max_results: int = 10
):

    if not prefix:
        return []


    try:

        response = requests.get(

            f"{BASE_URL}/sug",

            params={
                "s": prefix,
                "max": max_results
            },

            timeout=TIMEOUT
        )


        response.raise_for_status()

        return response.json()


    except Exception:

        return []


# ==========================================================
# GENERAL WORD SEARCH
# ==========================================================

def search_words(
        query: str,
        limit: int = 20
):

    return _query({

        "ml": query,
        "max": limit,
        "md": "psrf"

    })



# ==========================================================
# SYNONYMS
# ==========================================================

def synonyms(
        word: str,
        limit: int = 20
):

    return _query({

        "rel_syn": word,
        "max": limit,
        "md": "psrf"

    })


# ==========================================================
# ANTONYMS
# ==========================================================

def antonyms(
        word: str,
        limit: int = 20
):

    return _query({

        "rel_ant": word,
        "max": limit,
        "md": "psrf"

    })


# ==========================================================
# MEANING / SEMANTIC
# ==========================================================

def meaning(
        word: str,
        limit: int = 20
):

    return _query({

        "ml": word,
        "max": limit,
        "md": "psrf"

    })


# ==========================================================
# SOUNDS LIKE
# ==========================================================

def sounds_like(
        word: str,
        limit: int = 20
):

    return _query({

        "sl": word,
        "max": limit,
        "md": "psrf"

    })


# ==========================================================
# SPELL CHECK / SIMILAR SPELLING
# ==========================================================

def spelled_like(
        word: str,
        limit: int = 20
):

    return _query({

        "sp": word,
        "max": limit,
        "md": "psrf"

    })


# ==========================================================
# RHYMES
# ==========================================================

def rhymes(
        word: str,
        limit: int = 20
):

    return _query({

        "rel_rhy": word,
        "max": limit

    })


# ==========================================================
# HOMOPHONES
# ==========================================================

def homophones(
        word: str
):

    return _query({

        "rel_hom": word,
        "md": "psrf"

    })


# ==========================================================
# WORD ASSOCIATIONS
# ==========================================================

def related(
        word: str,
        limit: int = 20
):

    return _query({

        "rel_trg": word,
        "max": limit,
        "md": "psrf"

    })


# ==========================================================
# TAXONOMY
# ==========================================================

def kind_of(word: str):

    return _query({

        "rel_spc": word,
        "md": "psrf"

    })


def more_specific(word: str):

    return _query({

        "rel_gen": word,
        "md": "psrf"

    })


def part_of(word: str):

    return _query({

        "rel_par": word,
        "md": "psrf"

    })


def comprises(word: str):

    return _query({

        "rel_com": word,
        "md": "psrf"

    })


# ==========================================================
# LANGUAGE RELATIONSHIPS
# ==========================================================

def describing(word: str):

    return _query({

        "rel_jjb": word,
        "md": "psrf"

    })


def described_by(word: str):

    return _query({

        "rel_jja": word,
        "md": "psrf"

    })


def follows(word: str):

    return _query({

        "rel_bga": word,
        "md": "psrf"

    })


def precedes(word: str):

    return _query({

        "rel_bgb": word,
        "md": "psrf"

    })


# ==========================================================
# METADATA LOOKUP
# ==========================================================

def lookup(word: str):

    results = _query({

        "sp": word,
        "qe": "sp",
        "md": "dpsrf"

    })


    if results:
        return results[0]


    return {}



# ==========================================================
# HELPERS
# ==========================================================

def words_only(results):

    return [

        item["word"]

        for item in results

        if "word" in item

    ]



# ==========================================================
# GAME WORD GENERATOR
# ==========================================================

def game_words(pattern="*", category="general", limit=50):

    """
    Used for:

    - Hangman
    - Word Search
    - Crossword

    Example:

    game_words("c????")
    """

    if pattern != "*":
        candidates = words_only(_query({"sp": pattern, "max": limit}))
    else:
        categories = {
            "animal": "animal", "science": "science", "nature": "nature",
            "technology": "technology", "food": "food", "general": "language",
        }
        candidates = words_only(_query({"ml": categories.get(category, "language"), "max": limit, "md": "p"}))
    return [word.lower() for word in candidates if word.replace(" ", "").isalpha() and 3 <= len(word) <= 14]



# ==========================================================
# COMPLETE WORD PROFILE
# ==========================================================

def profile(word: str):
    """Compact profile used by the explorer (one request per displayed relation)."""
    return {
        "metadata": lookup(word),
        "synonyms": words_only(synonyms(word)),
        "antonyms": words_only(antonyms(word)),
        "meaning": words_only(meaning(word)),
        "related": words_only(related(word)),
        "rhymes": words_only(rhymes(word)),
        "homophones": words_only(homophones(word)),
        "kind_of": [], "more_specific": [], "part_of": [], "comprises": [],
        "describing": [], "described_by": [], "follows": [], "precedes": [],
    }



