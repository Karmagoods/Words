import streamlit as st
from games.crossword import DEFAULT_CLUES, check_answers
from utils.session import record_win

st.set_page_config(page_title="Crossword | Words", page_icon="🧩", layout="centered")
st.title("🧩 Mini Crossword")
st.caption("Solve each language-themed clue. This compact crossword works like a fill-in puzzle.")
answers = {}
for clue in DEFAULT_CLUES:
    answers[str(clue["number"])] = st.text_input(f"{clue['number']}. {clue['clue']} ({len(clue['answer'])})", key=f"crossword_{clue['number']}")
if st.button("Check crossword", use_container_width=True):
    correct, complete = check_answers(DEFAULT_CLUES, answers)
    if complete: record_win(45); st.success("Crossword complete — excellent work!")
    else: st.info(f"You have {len(correct)} of {len(DEFAULT_CLUES)} correct. Keep going.")
