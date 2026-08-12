import streamlit as st

from games.daily import challenge
from games.achievements import ACHIEVEMENTS, unlocked
from utils.session import stats
from services.word_engine import WordEngine

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
    padding-top:10px;
    padding-bottom:10px;
}

.hero h1{
    font-size:54px;
    color:#3A86FF;
    margin-bottom:0px;
}

.hero h3{
    color:#888;
    font-weight:400;
    margin-top:4px;
}

.game-card{
    padding:18px 16px;
    border-radius:14px;
    border:1px solid #3a3a3a;
    background-color:#1f1f1f;
    height:150px;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
}

.game-card h4{
    margin:0 0 4px 0;
    font-size:19px;
}

.game-card p{
    margin:0;
    color:#999;
    font-size:13px;
}

.badge{
    display:inline-block;
    padding:4px 10px;
    margin:2px;
    border-radius:999px;
    font-size:12px;
    background-color:#2a2a2a;
    color:#3A86FF;
    border:1px solid #3A86FF33;
}

.badge-locked{
    color:#666;
    border:1px solid #444;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HERO
# ==========================================================

st.markdown("""
<div class="hero">
<h1>📖 Words</h1>
<h3>Discover • Play • Understand Language</h3>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "An AI-powered linguistics playground — look up any word, then put it "
    "to the test in a spelling bee, a crossword, a word ladder, and more."
)

st.divider()

# ==========================================================
# LIVE DEMO — WORD LOOKUP
# ==========================================================

st.subheader("🔎 Try it now")

demo_col, daily_col = st.columns([2, 1])

with demo_col:
    word = st.text_input(
        "Look up a word",
        placeholder="e.g. photosynthesis",
        label_visibility="collapsed"
    )

    if word.strip():
        with st.spinner("Looking that up..."):
            data = WordEngine().search(word.strip())

        definitions = data.get("definitions", []) if data else []

        if definitions:
            top = definitions[0]
            st.markdown(f"**{word.title()}** — *{top.get('part_of_speech', 'word')}*")
            st.write(top.get("definition", ""))
            related = data.get("related", [])
            if related:
                st.caption("Related: " + ", ".join(related[:6]))
            st.page_link(
                "pages/Word_Explorer.py",
                label="See full breakdown in Word Explorer →",
                icon="🔍"
            )
        else:
            st.info("No definition found from live sources right now — try Word Explorer for more depth.")
    else:
        st.caption("Type any word above and press Enter for an instant definition.")

with daily_col:
    today = challenge()
    st.markdown("**✨ Word of the Day**")
    st.markdown(f"### {today['word'].title()}")
    st.page_link(
        "pages/Word_of_the_Day.py",
        label="Learn it",
        icon="✨"
    )
    st.page_link(
        "pages/Daily_Challenge.py",
        label="Play today's challenge",
        icon="📅"
    )

st.divider()

# ==========================================================
# GAMES GRID
# ==========================================================

st.subheader("🎮 Play a game")

games = [
    ("pages/Spelling_Bee.py", "🐝 Spelling Bee", "Build words from a hive of letters."),
    ("pages/Crossword.py", "🧩 Crossword", "A compact language-themed crossword."),
    ("pages/Word_Ladder.py", "🪜 Word Ladder", "Change one letter at a time to reach the target."),
    ("pages/Unscramble.py", "🔀 Unscramble", "Rearrange the letters to find the word."),
    ("pages/Word_Search.py", "🔎 Word Search", "Hunt for hidden words in the grid."),
    ("pages/Daily_Challenge.py", "📅 Daily Challenge", "One new puzzle, every day."),
]

cols = st.columns(3)
for i, (page, title, desc) in enumerate(games):
    with cols[i % 3]:
        st.markdown(
            f"""<div class="game-card"><div><h4>{title}</h4><p>{desc}</p></div></div>""",
            unsafe_allow_html=True
        )
        st.page_link(page, label="Play", icon="▶️", use_container_width=True)
        st.write("")

st.divider()

# ==========================================================
# PROGRESS
# ==========================================================

st.subheader("🏆 Your progress")

user_stats = stats()
earned = unlocked(user_stats)

p1, p2, p3 = st.columns(3)
p1.metric("Score", user_stats.get("score", 0))
p2.metric("Wins", user_stats.get("wins", 0))
p3.metric("Daily streak wins", user_stats.get("daily_wins", 0))

st.caption("Badges")
badge_html = ""
for key, label in ACHIEVEMENTS.items():
    css_class = "badge" if key in earned else "badge badge-locked"
    icon = "✓ " if key in earned else "🔒 "
    badge_html += f'<span class="{css_class}">{icon}{label}</span>'
st.markdown(badge_html, unsafe_allow_html=True)

st.divider()

# ==========================================================
# EXPLORE MORE
# ==========================================================

st.subheader("🧭 Explore further")

e1, e2, e3 = st.columns(3)
with e1:
    st.page_link("pages/Etymology.py", label="🌍 Etymology Explorer", icon="🌍")
    st.caption("Trace a word's history and cognates.")
with e2:
    st.page_link("pages/Sentence_Analyzer.py", label="🧠 Sentence Analyzer", icon="🧠")
    st.caption("Break a sentence down into its grammar.")
with e3:
    st.page_link("pages/AI_Tutor.py", label="🤖 AI Tutor", icon="🤖")
    st.caption("Ask for a plain-English explanation.")

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")
st.caption(
    "Words • AI Linguistics Explorer | Built with Streamlit, spaCy and Python"
)