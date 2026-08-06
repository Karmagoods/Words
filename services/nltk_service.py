"""
==========================================================
NLTK / WordNet Service
----------------------------------------------------------

Provides lexical information using WordNet.

Features
---------
✓ Definitions
✓ Synonyms
✓ Antonyms
✓ Hypernyms
✓ Hyponyms
✓ Meronyms
✓ Holonyms
✓ Examples
✓ Lemmas

==========================================================
"""

import nltk
from nltk.corpus import wordnet as wn

# ----------------------------------------------------------
# Downloads
# ----------------------------------------------------------

try:
    wn.synsets("dog")

except LookupError:

    nltk.download("wordnet")
    nltk.download("omw-1.4")


# ----------------------------------------------------------
# Synsets
# ----------------------------------------------------------

def get_synsets(word):

    return wn.synsets(word)


# ----------------------------------------------------------
# Definitions
# ----------------------------------------------------------

def get_definitions(word):

    definitions = []

    for synset in wn.synsets(word):

        definitions.append({

            "synset": synset.name(),

            "definition": synset.definition(),

            "examples": synset.examples()

        })

    return definitions


# ----------------------------------------------------------
# Synonyms
# ----------------------------------------------------------

def get_synonyms(word):

    synonyms = set()

    for synset in wn.synsets(word):

        for lemma in synset.lemmas():

            synonyms.add(lemma.name().replace("_", " "))

    return sorted(synonyms)


# ----------------------------------------------------------
# Antonyms
# ----------------------------------------------------------

def get_antonyms(word):

    antonyms = set()

    for synset in wn.synsets(word):

        for lemma in synset.lemmas():

            for ant in lemma.antonyms():

                antonyms.add(ant.name().replace("_", " "))

    return sorted(antonyms)


# ----------------------------------------------------------
# Hypernyms
# ----------------------------------------------------------

def get_hypernyms(word):

    words = set()

    for synset in wn.synsets(word):

        for hypernym in synset.hypernyms():

            words.add(hypernym.name().split(".")[0])

    return sorted(words)


# ----------------------------------------------------------
# Hyponyms
# ----------------------------------------------------------

def get_hyponyms(word):

    words = set()

    for synset in wn.synsets(word):

        for hyponym in synset.hyponyms():

            words.add(hyponym.name().split(".")[0])

    return sorted(words)


# ----------------------------------------------------------
# Meronyms
# ----------------------------------------------------------

def get_meronyms(word):

    words = set()

    for synset in wn.synsets(word):

        for item in synset.part_meronyms():

            words.add(item.name().split(".")[0])

    return sorted(words)


# ----------------------------------------------------------
# Holonyms
# ----------------------------------------------------------

def get_holonyms(word):

    words = set()

    for synset in wn.synsets(word):

        for item in synset.part_holonyms():

            words.add(item.name().split(".")[0])

    return sorted(words)


# ----------------------------------------------------------
# Examples
# ----------------------------------------------------------

def get_examples(word):

    examples = []

    for synset in wn.synsets(word):

        examples.extend(synset.examples())

    return examples


# ----------------------------------------------------------
# Complete Analysis
# ----------------------------------------------------------

def analyze(word):

    return {

        "word": word,

        "definitions": get_definitions(word),

        "synonyms": get_synonyms(word),

        "antonyms": get_antonyms(word),

        "hypernyms": get_hypernyms(word),

        "hyponyms": get_hyponyms(word),

        "meronyms": get_meronyms(word),

        "holonyms": get_holonyms(word),

        "examples": get_examples(word)

    }


# ----------------------------------------------------------
# Test
# ----------------------------------------------------------

if __name__ == "__main__":

    data = analyze("dog")

    print(data)