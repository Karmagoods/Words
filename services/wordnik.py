"""Optional Wordnik adapter.

The app works without a Wordnik key. Configure WORDNIK_API_KEY in
.streamlit/secrets.toml to enable the provider later.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def summarize(word: str) -> dict[str, Any] | None:
    """Return no data until a key-backed Wordnik client is configured."""
    _ = word
    if not st.secrets.get("WORDNIK_API_KEY", None):
        return None
    # A key is present, but no Wordnik client has been configured yet.
    # Returning None keeps Wordnik optional without masking import failures.
    return None
