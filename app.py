import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Words",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.hero {
    text-align:center;
    padding-top:20px;
    padding-bottom:20px;
}

.hero h1{
    font-size:58px;
    color:#3A86FF;
}

.hero h3{
    color:#888;
    font-weight:400;
}

.card{
    padding:20px;
    border-radius:12px;
    border:1px solid #444;
    min-height:250px;
}

.metric{
    text-align:center;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HERO
# ==========================================================

st.markdown("""
<div class="hero">

<h1>📖 Words</h1>

<h3>
Discover • Analyze • Understand Language
</h3>

</div>
""", unsafe_allow_html=True)

st.markdown(
    """
**Words** is an AI-powered linguistics explorer designed to help you investigate
the structure, meaning, history and relationships of words and phrases.

Whether you're a student, writer, teacher, translator or language enthusiast,
Words aims to become your complete language analysis toolkit.
"""
)

st.divider()

# ==========================================================
# FEATURES
# ==========================================================

st.header("✨ Current Features")

col1, col2, col3 = st.columns(3)

with col1:

    st.container(border=True)

    st.markdown("### 📖 Dictionary")

    st.write("✓ Definitions")
    st.write("✓ Parts of Speech")
    st.write("✓ IPA Pronunciation")
    st.write("✓ Audio Pronunciation")
    st.write("✓ Example Sentences")

with col2:

    st.container(border=True)

    st.markdown("### 🧩 Linguistics")

    st.write("✓ Lemmas")
    st.write("✓ Morphology")
    st.write("✓ Token Analysis")
    st.write("✓ Dependency Parsing")
    st.write("✓ Named Entities")

with col3:

    st.container(border=True)

    st.markdown("### 🧠 AI")

    st.write("🚧 AI Explanations")
    st.write("🚧 Etymology")
    st.write("🚧 Word Families")
    st.write("🚧 Semantic Networks")
    st.write("🚧 Syntax Trees")

st.divider()

# ==========================================================
# ROADMAP
# ==========================================================

st.header("🗺 Development Roadmap")

roadmap = [

    "✅ Dictionary Integration",
    "✅ spaCy NLP",
    "✅ Morphology",

    "🔄 WordNet",

    "🔄 Etymology",

    "🔄 AI Explanations",

    "🔄 Sentence Analysis",

    "🔄 Syntax Trees",

    "🔄 Translation",

    "🔄 Semantic Graphs",

    "🔄 Historical Word Usage",

    "🔄 Language Family Explorer"

]

for item in roadmap:
    st.write(item)

st.divider()

# ==========================================================
# PROJECT STATS
# ==========================================================

st.header("📊 Project")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Pages", "5")
c2.metric("Services", "2")
c3.metric("Languages", "English")
c4.metric("Status", "Alpha")

st.divider()

# ==========================================================
# QUICK START
# ==========================================================

st.success("""
### 🚀 Getting Started

Use the **sidebar** to open:

- 🏠 Home
- 🔎 Word Explorer
- 🌍 Etymology
- 🧠 Sentence Analyzer
- ℹ About

Start with **Word Explorer** and enter any word or phrase.
""")

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
    "Words • AI Linguistics Explorer | Built with Streamlit, spaCy and Python"
)