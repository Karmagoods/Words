import streamlit as st
from games.base_game import choose_word
from games.unscramble import scramble, is_correct
from utils.session import get, put, record_win

st.set_page_config(page_title="Unscramble | Words", page_icon="🔀", layout="centered")
st.title("🔀 Unscramble")
if st.button("New word", use_container_width=True) or not get("unscramble_word"):
    word = choose_word(); put("unscramble_word", word); put("unscramble_letters", scramble(word)); put("unscramble_done", False)
word = get("unscramble_word")
st.caption("Rearrange the letters to make a word.")
st.markdown(f"## {' · '.join(get('unscramble_letters'))}")
answer = st.text_input("Your answer", disabled=get("unscramble_done", False))
if st.button("Check answer", use_container_width=True) and not get("unscramble_done", False):
    if is_correct(answer, word): put("unscramble_done", True); record_win(15); st.success(f"Correct — **{word}**!")
    else: st.warning("Not quite. Try another arrangement.")
