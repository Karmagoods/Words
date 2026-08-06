"""
==========================================================
Dictionary Aggregator
----------------------------------------------------------
Central service for all linguistic providers.

Providers
---------
✓ Free Dictionary API
✓ Datamuse
✓ Wordnik
✓ Wiktionary
✓ Etymonline
✓ AI fallback

Returns one unified dictionary object for the UI.
==========================================================
"""

from services.free_dictionary import summarize as free_dictionary

try:
    from services.datamuse import summarize as datamuse
except Exception:
    datamuse = None

try:
    from services.wordnik import summarize as wordnik
except Exception:
    wordnik = None

try:
    from services.etymology import summarize as etymology
except Exception:
    etymology = None

try:
    from services.ai_service import summarize as ai_summary
except Exception:
    ai_summary = None


# ----------------------------------------------------------
# Helpers
# ----------------------------------------------------------

def merge_lists(*lists):
    """
    Merge lists removing duplicates while preserving order.
    """

    seen = set()
    output = []

    for lst in lists:

        if not lst:
            continue

        for item in lst:

            if item and item not in seen:

                seen.add(item)
                output.append(item)

    return output


# ----------------------------------------------------------
# Summary
# ----------------------------------------------------------

def summarize(word: str):

    result = {

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

    # --------------------------------------------------
    # Free Dictionary
    # --------------------------------------------------

    try:

        data = free_dictionary(word)

        if data:

            result["word"] = data.get("word", word)

            result["ipa"] = data.get("ipa")

            result["audio"] = data.get("audio")

            result["definitions"] = data.get("definitions", [])

            result["synonyms"] = data.get("synonyms", [])

            result["antonyms"] = data.get("antonyms", [])

            result["examples"] = [

                d["example"]

                for d in data.get("definitions", [])

                if d.get("example")

            ]

    except Exception:
        pass

    # --------------------------------------------------
    # Datamuse
    # --------------------------------------------------

    if datamuse:

        try:

            dm = datamuse(word)

            if dm:

                result["related"] = dm.get("related", [])

                result["sounds_like"] = dm.get("sounds_like", [])

                result["rhymes"] = dm.get("rhymes", [])

                result["triggers"] = dm.get("triggers", [])

                result["adjectives"] = dm.get("adjectives", [])

                result["nouns"] = dm.get("nouns", [])

                result["frequency"] = dm.get("frequency")

                result["syllables"] = dm.get("syllables")

        except Exception:
            pass

    # --------------------------------------------------
    # Wordnik
    # --------------------------------------------------

    if wordnik:

        try:

            wk = wordnik(word)

            if wk:

                result["examples"] = merge_lists(
                    result["examples"],
                    wk.get("examples", [])
                )

                if not result["ipa"]:
                    result["ipa"] = wk.get("ipa")

        except Exception:
            pass

    # --------------------------------------------------
    # Etymology
    # --------------------------------------------------

    if etymology:

        try:

            ety = etymology(word)

            if ety:

                result["etymology"] = ety.get("etymology")

        except Exception:
            pass

    # --------------------------------------------------
    # AI fallback
    # --------------------------------------------------

    if not result["definitions"] and ai_summary:

        try:

            ai = ai_summary(word)

            if ai:

                result["definitions"] = ai.get(
                    "definitions",
                    []
                )

        except Exception:
            pass

    # --------------------------------------------------
    # Cleanup
    # --------------------------------------------------

    result["synonyms"] = merge_lists(result["synonyms"])

    result["antonyms"] = merge_lists(result["antonyms"])

    result["examples"] = merge_lists(result["examples"])

    result["related"] = merge_lists(result["related"])

    result["sounds_like"] = merge_lists(result["sounds_like"])

    result["rhymes"] = merge_lists(result["rhymes"])

    result["triggers"] = merge_lists(result["triggers"])

    result["adjectives"] = merge_lists(result["adjectives"])

    result["nouns"] = merge_lists(result["nouns"])

    return result


# ----------------------------------------------------------
# Test
# ----------------------------------------------------------

if __name__ == "__main__":

    from pprint import pprint

    pprint(summarize("language"))