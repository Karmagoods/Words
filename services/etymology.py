"""
==========================================================
Etymology Service
----------------------------------------------------------
Provides etymological information for the Words app.

Version 1

✓ Service structure
✓ Ready for multiple providers
✓ Cached requests
✓ Graceful error handling

Future

- Wiktionary
- AI summaries
- Language family detection
- Word evolution timeline
- Cognates
- Historical pronunciation
==========================================================
"""

import requests
import streamlit as st

# ----------------------------------------------------------
# Configuration
# ----------------------------------------------------------

WIKTIONARY_API = "https://en.wiktionary.org/w/api.php"


# ----------------------------------------------------------
# Helpers
# ----------------------------------------------------------

def empty_result(word: str):
    """
    Default empty response.
    """

    return {
        "word": word,
        "origin": None,
        "language": None,
        "family": None,
        "timeline": [],
        "history": None,
        "cognates": [],
        "related_words": [],
        "summary": None
    }


# ----------------------------------------------------------
# Wiktionary Lookup
# ----------------------------------------------------------

@st.cache_data(show_spinner=False)
def lookup_wiktionary(word: str):
    """
    Retrieve the raw Wiktionary page.

    NOTE:
    This is the foundation for future parsing.
    """

    params = {
        "action": "parse",
        "page": word,
        "prop": "text",
        "format": "json"
    }

    try:

        response = requests.get(
            WIKTIONARY_API,
            params=params,
            timeout=15
        )

        if response.status_code != 200:
            return None

        return response.json()

    except Exception:

        return None


# ----------------------------------------------------------
# Main Lookup
# ----------------------------------------------------------

def get_etymology(word: str):
    """
    Main service entry point.

    Returns a standardized dictionary regardless of
    the provider used.
    """

    result = empty_result(word)

    raw = lookup_wiktionary(word)

    if raw is None:
        return result

    # --------------------------------------------------
    # Placeholder
    # Future HTML parsing will happen here.
    # --------------------------------------------------

    result["summary"] = (
        "Wiktionary page located successfully. "
        "Detailed etymology parsing will be implemented "
        "in the next version."
    )

    return result


# ----------------------------------------------------------
# Timeline
# ----------------------------------------------------------

def get_timeline(word: str):
    """
    Placeholder timeline.
    """

    return [
        {
            "period": "Proto Language",
            "language": "Unknown",
            "word": None
        },
        {
            "period": "Ancient",
            "language": "Unknown",
            "word": None
        },
        {
            "period": "Medieval",
            "language": "Unknown",
            "word": None
        },
        {
            "period": "Modern",
            "language": "English",
            "word": word
        }
    ]


# ----------------------------------------------------------
# Language Family
# ----------------------------------------------------------

def get_language_family(language: str):
    """
    Very small starter dataset.
    """

    families = {

        "English": "Germanic",

        "German": "Germanic",

        "Dutch": "Germanic",

        "French": "Romance",

        "Spanish": "Romance",

        "Italian": "Romance",

        "Latin": "Italic",

        "Greek": "Hellenic",

        "Sanskrit": "Indo-Aryan"

    }

    return families.get(language)


# ----------------------------------------------------------
# AI Summary Placeholder
# ----------------------------------------------------------

def generate_summary(data):
    """
    Placeholder for future AI integration.
    """

    if not data:
        return None

    return data.get("summary")


# ----------------------------------------------------------
# Complete Analysis
# ----------------------------------------------------------

def analyze(word: str):
    """
    One function that returns everything.

    This is the only function the UI should call.
    """

    result = get_etymology(word)

    result["timeline"] = get_timeline(word)

    return result


# ----------------------------------------------------------
# Test
# ----------------------------------------------------------

if __name__ == "__main__":

    data = analyze("language")

    print(data)