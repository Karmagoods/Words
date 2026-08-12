import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="Words | How it works",
    page_icon="📖",
    layout="wide"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================
st.markdown("""
<style>

.main-title{
    font-size:44px;
    font-weight:700;
    color:#3A86FF;
    margin-bottom:0px;
}

.subtitle{
    font-size:20px;
    color:#888888;
    margin-top:4px;
}

.pillar-card{
    padding:22px;
    border-radius:15px;
    border:1px solid #444;
    background-color:#1f1f1f;
    height:230px;
}

.pillar-card h3{
    margin-top:0;
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

st.markdown('<p class="main-title">📖 How Words works</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">One toolkit, three ways to explore language.</p>',
    unsafe_allow_html=True
)

st.divider()

# ==========================================================
# THREE PILLARS
# ==========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """<div class="pillar-card">
        <h3>🔍 Look it up</h3>
        <p>Type any word or phrase and get a real definition, part of speech,
        synonyms, and related words in seconds — no ad-cluttered dictionary
        sites required.</p>
        </div>""",
        unsafe_allow_html=True
    )
    st.write("")
    st.page_link("pages/Word_Explorer.py", label="Open Word Explorer", icon="🔍")

with col2:
    st.markdown(
        """<div class="pillar-card">
        <h3>🎮 Play with it</h3>
        <p>Turn what you've learned into practice with a Spelling Bee,
        Crossword, Word Ladder, Word Search, Unscramble, or the Daily
        Challenge — each one tracks your score and badges.</p>
        </div>""",
        unsafe_allow_html=True
    )
    st.write("")
    st.page_link("pages/Daily_Challenge.py", label="Play today's challenge", icon="📅")

with col3:
    st.markdown(
        """<div class="pillar-card">
        <h3>🧠 Understand it</h3>
        <p>Trace a word's origins in the Etymology Explorer, break a full
        sentence down grammatically, or ask the AI Tutor for a plain-English
        explanation.</p>
        </div>""",
        unsafe_allow_html=True
    )
    st.write("")
    st.page_link("pages/Etymology.py", label="Open Etymology Explorer", icon="🌍")

st.divider()

# ==========================================================
# WHAT'S UNDER THE HOOD
# ==========================================================

st.header("⚙️ What's under the hood")

tech1, tech2 = st.columns(2)

with tech1:
    st.markdown("""
**Language data**
- Dictionary definitions & example sentences
- Datamuse word relationships
- WordNet synonym/antonym networks
- Etymology sources
""")

with tech2:
    st.markdown("""
**Analysis**
- spaCy for tokens, morphology & dependency parsing
- NLTK for supporting NLP tasks
- Groq-powered AI explanations (optional, needs a key)
""")

st.caption(
    "Curious about the roadmap, tech stack, and what's still in progress? "
    "See the [About page](/About) for the full picture."
)

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
    unsafe_allow_html=True
)