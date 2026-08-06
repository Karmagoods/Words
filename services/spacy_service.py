"""
==========================================================
spaCy Service
----------------------------------------------------------
Provides NLP functions for the Words application.

Features
---------
✓ Tokenization
✓ Lemmatization
✓ Part of Speech
✓ Morphological Features
✓ Dependency Parsing
✓ Named Entity Recognition
✓ Sentence Detection
==========================================================
"""

import spacy
import streamlit as st

# ----------------------------------------------------------
# Load Model (cached)
# ----------------------------------------------------------

@st.cache_resource
def load_model():
    """
    Load the spaCy English language model.
    """
    return spacy.load("en_core_web_sm")


nlp = load_model()

# ----------------------------------------------------------
# Main Analysis
# ----------------------------------------------------------

def analyze_text(text: str):
    """
    Analyze text using spaCy.

    Returns:
        spaCy Doc object
    """
    return nlp(text)


# ----------------------------------------------------------
# Token Information
# ----------------------------------------------------------

def get_tokens(doc):
    """
    Return detailed information for every token.
    """

    tokens = []

    for token in doc:

        tokens.append({

            "text": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "tag": token.tag_,
            "dependency": token.dep_,
            "head": token.head.text,
            "shape": token.shape_,
            "is_alpha": token.is_alpha,
            "is_stopword": token.is_stop,
            "morphology": str(token.morph)

        })

    return tokens


# ----------------------------------------------------------
# Named Entities
# ----------------------------------------------------------

def get_entities(doc):

    entities = []

    for ent in doc.ents:

        entities.append({

            "text": ent.text,
            "label": ent.label_,
            "description": spacy.explain(ent.label_)

        })

    return entities


# ----------------------------------------------------------
# Sentences
# ----------------------------------------------------------

def get_sentences(doc):

    return [sent.text for sent in doc.sents]


# ----------------------------------------------------------
# Morphology
# ----------------------------------------------------------

def get_morphology(doc):

    morphology = []

    for token in doc:

        morphology.append({

            "word": token.text,
            "lemma": token.lemma_,
            "morphology": str(token.morph)

        })

    return morphology


# ----------------------------------------------------------
# Part of Speech
# ----------------------------------------------------------

def get_part_of_speech(doc):

    results = []

    for token in doc:

        results.append({

            "word": token.text,
            "pos": token.pos_,
            "description": spacy.explain(token.pos_)

        })

    return results


# ----------------------------------------------------------
# Dependency Parsing
# ----------------------------------------------------------

def get_dependencies(doc):

    dependencies = []

    for token in doc:

        dependencies.append({

            "word": token.text,
            "dependency": token.dep_,
            "description": spacy.explain(token.dep_),
            "head": token.head.text

        })

    return dependencies


# ----------------------------------------------------------
# Quick Summary
# ----------------------------------------------------------

def get_summary(text: str):
    """
    Returns a compact overview of the analysis.
    """

    doc = analyze_text(text)

    return {

        "text": text,
        "tokens": len(doc),
        "sentences": len(list(doc.sents)),
        "entities": len(doc.ents),
        "words": [token.text for token in doc]

    }


# ----------------------------------------------------------
# Test
# ----------------------------------------------------------

if __name__ == "__main__":

    sample = "The quick brown fox jumps over the lazy dog."

    doc = analyze_text(sample)

    print(get_summary(sample))
    print(get_tokens(doc))