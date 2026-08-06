import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="Words | Home",
    page_icon="📖",
    layout="wide"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================
st.markdown("""
<style>

.main-title{
    font-size:48px;
    font-weight:700;
    color:#3A86FF;
}

.subtitle{
    font-size:22px;
    color:#888888;
}

.feature-card{
    padding:20px;
    border-radius:15px;
    border:1px solid #444;
    background-color:#1f1f1f;
    margin-bottom:15px;
}

.footer{
    text-align:center;
    color:grey;
    padding-top:40px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    '<p class="main-title">📖 Words</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Discover the science, history and beauty of language.</p>',
    unsafe_allow_html=True
)

st.divider()

# ==========================================================
# INTRODUCTION
# ==========================================================

st.markdown("""
Welcome to **Words**, an AI-powered linguistics explorer.

Whether you're a student, teacher, writer, linguist, translator, or simply curious,
Words helps you explore language in ways ordinary dictionaries cannot.

Enter a single word, an idiom, or an entire sentence and uncover its hidden structure.
""")

st.divider()

# ==========================================================
# FEATURES
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 🔍 Explore Words")

    st.info("""
• Dictionary definitions

• Parts of speech

• Morphology

• Prefixes & suffixes

• Word roots

• Synonyms & antonyms

• Usage examples
""")

    st.markdown("### 🧠 AI Analysis")

    st.info("""
• Plain-English explanations

• Educational summaries

• Word families

• Related concepts

• Learning insights
""")

with col2:

    st.markdown("### 🌍 Language History")

    st.info("""
• Etymology

• Language origins

• Historical development

• Timeline of evolution

• Cognates
""")

    st.markdown("### ✍ Sentence Analysis")

    st.info("""
• Syntax

• Grammar

• Dependency parsing

• Phrase structure

• Sentence diagrams
""")

st.divider()

# ==========================================================
# COMING SOON
# ==========================================================

st.markdown("## 🚀 Planned Features")

features = [
    "IPA pronunciation",
    "Interactive syntax trees",
    "Historical word usage",
    "Language family explorer",
    "Semantic relationship graphs",
    "Translation into multiple languages",
    "AI writing assistant",
    "Word comparison mode",
    "Idiom explorer",
    "Corpus search",
]

for feature in features:
    st.checkbox(feature, value=False, disabled=True)

st.divider()

# ==========================================================
# QUICK START
# ==========================================================

st.success("""
### Getting Started

1. Open **Word Explorer** from the sidebar.

2. Type any word or phrase.

3. Explore its meaning, structure, and history.

4. Try a sentence to discover its grammar and syntax.
""")

# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    """
<div class='footer'>
Built with ❤️ using Streamlit<br>
Words • AI Linguistics Explorer
</div>
""",
unsafe_allow_html=True)