import streamlit as st
from games.spelling_bee import BEE_PUZZLES, valid_bee_word, is_pangram
from utils.session import get, put, record_win

st.set_page_config(page_title="Spelling Bee | Words", page_icon="🐝", layout="centered")
st.title("🐝 Spelling Bee")
if st.button("New puzzle", use_container_width=True) or not get("bee"):
    index = (get("bee_index", -1) + 1) % len(BEE_PUZZLES); put("bee_index", index); put("bee", BEE_PUZZLES[index]); put("bee_found", set())
puzzle, found = get("bee"), get("bee_found")
st.caption(f"Make words of 4+ letters using only these letters. Every word must include **{puzzle['center'].upper()}**.")
st.markdown("## " + " · ".join(letter.upper() for letter in puzzle["letters"]))
answer = st.text_input("Word")
if st.button("Submit word", use_container_width=True):
    answer = answer.lower()
    if answer in found: st.info("Already found.")
    elif answer not in puzzle["words"]: st.warning("That isn't one of this puzzle's accepted words.")
    elif not valid_bee_word(answer, puzzle["letters"], puzzle["center"]): st.warning("Use the displayed letters and include the centre letter.")
    else:
        found.add(answer); put("bee_found", found); record_win(7 + (7 if is_pangram(answer, puzzle['letters']) else 0)); st.success("Accepted!")
st.write(f"Found {len(found)} of {len(puzzle['words'])}: " + (", ".join(sorted(found)) or "none yet"))
