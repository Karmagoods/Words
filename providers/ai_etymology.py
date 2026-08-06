"""
==========================================================
AI Etymology Service
----------------------------------------------------------

Uses an LLM to explain the history of a word in
easy-to-understand language.

Version 1

✓ Prompt Builder
✓ Provider Agnostic
✓ Ready for Groq/OpenAI/OpenRouter

Future

- Timeline generation
- Language family explanations
- Historical pronunciation
- Interactive learning mode
==========================================================
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ----------------------------------------------------------
# Configuration
# ----------------------------------------------------------

AI_PROVIDER = os.getenv("AI_PROVIDER", "none").lower()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


# ----------------------------------------------------------
# Prompt Builder
# ----------------------------------------------------------

def build_prompt(word: str, etymology: dict | None = None):
    """
    Build a prompt for the LLM.
    """

    context = ""

    if etymology:

        context = f"""
Known information:

Origin: {etymology.get('origin')}
Language: {etymology.get('language')}
Family: {etymology.get('family')}
History:
{etymology.get('history')}
"""

    prompt = f"""
You are a professional historical linguist.

Explain the history of the word:

"{word}"

{context}

Requirements

- Be historically accurate.
- Do not invent facts.
- If information is uncertain, clearly say so.
- Explain in plain English.
- Mention important historical languages.
- Mention semantic changes.
- Maximum 250 words.
"""

    return prompt.strip()


# ----------------------------------------------------------
# Placeholder Provider
# ----------------------------------------------------------

def explain(word: str, etymology: dict | None = None):
    """
    Version 1 placeholder.

    Later this function will call Groq,
    OpenAI or another provider.
    """

    prompt = build_prompt(word, etymology)

    return {
        "provider": AI_PROVIDER,
        "word": word,
        "prompt": prompt,
        "response": (
            "AI explanations are not yet connected.\n\n"
            "The prompt has been generated successfully and "
            "is ready to be sent to an LLM."
        )
    }


# ----------------------------------------------------------
# Test
# ----------------------------------------------------------

if __name__ == "__main__":

    result = explain("language")

    print(result["response"])