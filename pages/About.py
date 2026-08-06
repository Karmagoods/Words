import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="About Words",
    page_icon="ℹ️",
    layout="wide"
)

# ==========================================================
# HEADER
# ==========================================================

st.title("ℹ️ About Words")

st.markdown("""
## Discover the Science of Language

**Words** is an AI-powered linguistics platform designed to help people
explore language beyond traditional dictionaries.

Rather than simply defining words, Words investigates how language is
constructed, how it has evolved over thousands of years, and how words
relate to one another across cultures and languages.
""")

st.divider()

# ==========================================================
# MISSION
# ==========================================================

st.header("🎯 Our Mission")

st.info("""
To make linguistics accessible, interactive, and enjoyable for everyone.

Whether you're learning a new language, writing a novel, teaching grammar,
or researching etymology, Words aims to become your complete language
companion.
""")

# ==========================================================
# WHAT WORDS CAN DO
# ==========================================================

st.header("📚 Current Features")

col1, col2 = st.columns(2)

with col1:

    st.success("Dictionary Definitions")
    st.success("Part of Speech")
    st.success("Lemmatization")
    st.success("Morphological Analysis")
    st.success("Dependency Parsing")
    st.success("Named Entity Recognition")

with col2:

    st.success("IPA Pronunciation")
    st.success("Synonyms")
    st.success("Antonyms")
    st.success("Example Sentences")
    st.success("Sentence Analysis")
    st.success("Token Analysis")

st.divider()

# ==========================================================
# ROADMAP
# ==========================================================

st.header("🚀 Roadmap")

roadmap = [

    "Interactive Syntax Trees",

    "Word Evolution Timelines",

    "AI Linguistics Tutor",

    "Etymology Explorer",

    "Language Family Trees",

    "Semantic Relationship Graphs",

    "Historical Usage",

    "Translation",

    "Phonetics & Pronunciation",

    "Corpus Search",

    "Multi-language Support"

]

for item in roadmap:

    st.checkbox(item, value=False, disabled=True)

st.divider()

# ==========================================================
# TECHNOLOGY
# ==========================================================

st.header("⚙️ Technology Stack")

tech1, tech2 = st.columns(2)

with tech1:

    st.markdown("""
### Core

- Python
- Streamlit
- spaCy
- pandas
- requests
""")

with tech2:

    st.markdown("""
### Planned

- WordNet
- Plotly
- NetworkX
- AI Language Models
- Wiktionary
""")

st.divider()

# ==========================================================
# WHY THIS PROJECT
# ==========================================================

st.header("💡 Why Words?")

st.write("""
Language is one of humanity's greatest inventions.

Every word has a history.
Every sentence has structure.
Every language tells the story of the people who speak it.

Words was created to help explore those stories through modern
Artificial Intelligence and Natural Language Processing.
""")

st.divider()

# ==========================================================
# VERSION
# ==========================================================

st.header("📦 Version")

c1, c2, c3 = st.columns(3)

c1.metric("Version", "0.1.0 Alpha")
c2.metric("Language", "English")
c3.metric("Status", "In Development")

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    "Words • AI Linguistics Explorer\n"
    "Built with ❤️ using Streamlit, spaCy and Python"
)