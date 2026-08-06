"""
==========================================================
Datamuse Service
----------------------------------------------------------
Wrapper around the Datamuse API.

Documentation:
https://www.datamuse.com/api/

No API key required until Jan 2027.
==========================================================
"""

from typing import List, Dict
import requests

BASE_URL = "https://api.datamuse.com"

TIMEOUT = 15


# ==========================================================
# INTERNAL REQUEST
# ==========================================================

def _query(params: Dict) -> List[Dict]:
    """
    Execute a Datamuse query.
    """

    try:

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

def autocomplete(prefix: str, max_results: int = 10):

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
# SYNONYMS
# ==========================================================

def synonyms(word: str, limit: int = 20):

    return _query({
        "rel_syn": word,
        "max": limit,
        "md": "psrf"
    })


# ==========================================================
# ANTONYMS
# ==========================================================

def antonyms(word: str, limit: int = 20):

    return _query({
        "rel_ant": word,
        "max": limit,
        "md": "psrf"
    })


# ==========================================================
# MEANS LIKE
# ==========================================================

def meaning(word: str, limit: int = 20):

    return _query({
        "ml": word,
        "max": limit,
        "md": "psrf"
    })


# ==========================================================
# SOUNDS LIKE
# ==========================================================

def sounds_like(word: str, limit: int = 20):

    return _query({
        "sl": word,
        "max": limit,
        "md": "psrf"
    })


# ==========================================================
# SPELLED LIKE
# ==========================================================

def spelled_like(word: str, limit: int = 20):

    return _query({
        "sp": word,
        "max": limit,
        "md": "psrf"
    })


# ==========================================================
# RHYMES
# ==========================================================

def rhymes(word: str, limit: int = 20):

    return _query({
        "rel_rhy": word,
        "max": limit,
        "md": "psrf"
    })


# ==========================================================
# HOMOPHONES
# ==========================================================

def homophones(word: str):

    return _query({
        "rel_hom": word,
        "md": "psrf"
    })


# ==========================================================
# TRIGGERS
# ==========================================================

def related(word: str, limit: int = 20):

    return _query({
        "rel_trg": word,
        "max": limit,
        "md": "psrf"
    })


# ==========================================================
# HYPERNYMS
# ==========================================================

def kind_of(word: str):

    return _query({
        "rel_spc": word,
        "md": "psrf"
    })


# ==========================================================
# HYPONYMS
# ==========================================================

def more_specific(word: str):

    return _query({
        "rel_gen": word,
        "md": "psrf"
    })


# ==========================================================
# MERONYMS
# ==========================================================

def part_of(word: str):

    return _query({
        "rel_par": word,
        "md": "psrf"
    })


# ==========================================================
# HOLONYMS
# ==========================================================

def comprises(word: str):

    return _query({
        "rel_com": word,
        "md": "psrf"
    })


# ==========================================================
# ADJECTIVES FOR NOUN
# ==========================================================

def describing(word: str):

    return _query({
        "rel_jjb": word,
        "md": "psrf"
    })


# ==========================================================
# NOUNS DESCRIBED BY ADJECTIVE
# ==========================================================

def described_by(word: str):

    return _query({
        "rel_jja": word,
        "md": "psrf"
    })


# ==========================================================
# FOLLOWING WORDS
# ==========================================================

def follows(word: str):

    return _query({
        "rel_bga": word,
        "md": "psrf"
    })


# ==========================================================
# PRECEDING WORDS
# ==========================================================

def precedes(word: str):

    return _query({
        "rel_bgb": word,
        "md": "psrf"
    })


# ==========================================================
# LOOKUP WORD METADATA
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
# SIMPLE LIST HELPER
# ==========================================================

def words_only(results):

    return [
        item["word"]
        for item in results
        if "word" in item
    ]


# ==========================================================
# COMPLETE WORD PROFILE
# ==========================================================

def profile(word: str):

    """
    Returns a complete Datamuse profile for one word.
    """

    return {

        "metadata": lookup(word),

        "synonyms": words_only(synonyms(word)),

        "antonyms": words_only(antonyms(word)),

        "meaning": words_only(meaning(word)),

        "related": words_only(related(word)),

        "rhymes": words_only(rhymes(word)),

        "homophones": words_only(homophones(word)),

        "kind_of": words_only(kind_of(word)),

        "more_specific": words_only(more_specific(word)),

        "part_of": words_only(part_of(word)),

        "comprises": words_only(comprises(word)),

        "describing": words_only(describing(word)),

        "described_by": words_only(described_by(word)),

        "follows": words_only(follows(word)),

        "precedes": words_only(precedes(word)),
    }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    word = "ocean"

    data = profile(word)

    from pprint import pprint

    pprint(data)