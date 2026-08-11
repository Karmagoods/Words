import streamlit as st
from games.daily import challenge
from games.unscramble import scramble, is_correct
from utils.session import get, put, record_win

st.set_page_config(page_title="Daily Challenge | Words", page_icon="📅", layout="centered")
st.title("📅 Daily Challenge")
today = challenge()
st.caption(f"{today['date']} · The same puzzle is shown all day.")
if get("daily_date") != today["date"]:
    put("daily_date", today["date"]); put("daily_letters", scramble(today["word"])); put("daily_done", False)
st.markdown("## " + " · ".join(get("daily_letters")))
st.write(today["hint"])
answer = st.text_input("Daily answer", disabled=get("daily_done", False))
if st.button("Submit daily answer", use_container_width=True) and not get("daily_done", False):
    if is_correct(answer, today["word"]): put("daily_done", True); record_win(30, daily=True); st.success("Daily challenge complete! Come back tomorrow for a new word.")
    else: st.warning("Not quite — try again.")
