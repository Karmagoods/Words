import streamlit as st
from games.daily import challenge
from services.word_engine import WordEngine

st.set_page_config(page_title="Word of the Day | Words", page_icon="✨", layout="centered")
st.title("✨ Word of the Day")
word = challenge()["word"]
st.markdown(f"## {word.title()}")
with st.spinner("Loading today’s word..."): data = WordEngine().search(word)
definitions = data.get("definitions", []) if data else []
if definitions:
    for item in definitions[:3]: st.write(f"**{item.get('part_of_speech', 'Word')}** — {item.get('definition', '')}")
else: st.info("Definition service is unavailable right now; today’s word is still ready to play in the Daily Challenge.")
if data:
    st.write("**Related:** " + ", ".join(data.get("related", [])[:8]))
    st.write("**Rhymes:** " + ", ".join(data.get("rhymes", [])[:8]))
