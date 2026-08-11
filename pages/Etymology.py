import streamlit as st
from services.etymology import analyze

st.set_page_config(page_title="Etymology | Words", page_icon="🌍", layout="wide")
st.title("🌍 Etymology Explorer")
st.caption("Explore the historical journey of a word. Results depend on the public source being available.")
word = st.text_input("Enter a word", placeholder="language")
if st.button("Explore origins", use_container_width=True):
    if not word.strip(): st.warning("Please enter a word.")
    else:
        with st.spinner("Looking through available sources..."): result = analyze(word.strip())
        left, right = st.columns([2, 1])
        with left:
            st.subheader("Word history")
            st.write(result.get("history") or result.get("summary") or "No detailed historical note is available for this word.")
            st.subheader("Timeline")
            for stage in result.get("timeline", []): st.write(f"• **{stage.get('period', 'History')}** — {stage.get('language') or 'Unknown'} {stage.get('word') or ''}")
        with right:
            st.metric("Language family", result.get("family") or "Unknown")
            st.metric("Root language", result.get("language") or "Unknown")
            st.subheader("Cognates")
            st.write(", ".join(result.get("cognates", [])) or "None found")
            st.subheader("Related words")
            st.write(", ".join(result.get("related_words", [])) or "None found")
else: st.info("Enter a word to explore its origins.")
