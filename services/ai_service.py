"""
==========================================================
AI Service
----------------------------------------------------------

Central AI gateway for the Words application.

Supported Providers
-------------------
✓ Groq

Future
------
- OpenAI
- Anthropic
- OpenRouter
- Ollama
- LM Studio

==========================================================
"""

from __future__ import annotations

from typing import Optional

import streamlit as st
from groq import Groq


# ==========================================================
# CONFIG
# ==========================================================

AI_PROVIDER = st.secrets.get("AI_PROVIDER", "groq")

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")

GROQ_MODEL = st.secrets.get(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)


# ==========================================================
# CLIENT
# ==========================================================

@st.cache_resource
def get_client():

    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY not found in .streamlit/secrets.toml"
        )

    return Groq(api_key=GROQ_API_KEY)


# ==========================================================
# ASK GROQ
# ==========================================================

def ask_groq(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 1000,
):

    client = get_client()

    messages = []

    if system_prompt:

        messages.append(
            {
                "role": "system",
                "content": system_prompt
            }
        )

    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    response = client.chat.completions.create(

        model=GROQ_MODEL,

        messages=messages,

        temperature=temperature,

        max_completion_tokens=max_tokens

    )

    return response.choices[0].message.content


# ==========================================================
# MAIN ENTRY POINT
# ==========================================================

def ask_ai(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 1000,
):

    provider = AI_PROVIDER.lower()

    if provider == "groq":

        return ask_groq(
            prompt,
            system_prompt,
            temperature,
            max_tokens
        )

    raise ValueError(
        f"Unsupported AI provider: {provider}"
    )


# ==========================================================
# LINGUISTICS HELPERS
# ==========================================================

def explain_word(word: str):

    prompt = f"""
Explain the word "{word}".

Include:

• Meaning
• Morphology
• Etymology
• Interesting facts

Keep it concise.
"""

    return ask_ai(prompt)


def explain_sentence(sentence: str):

    prompt = f"""
Explain this sentence like a linguistics professor.

Sentence:

{sentence}

Discuss:

- Grammar

- Syntax

- Semantics

- Style

- Interesting observations
"""

    return ask_ai(prompt)


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print(
        explain_word("language")
    )