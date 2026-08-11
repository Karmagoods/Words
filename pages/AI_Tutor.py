import streamlit as st
from services.ai_service import ask_ai

st.set_page_config(page_title="AI Tutor | Words", page_icon="🤖", layout="centered")
st.title("🤖 AI Tutor")
st.caption("Ask for a clear explanation of a word, grammar point, or sentence. The tutor is optional and needs a privately configured AI key.")
question = st.text_area("What would you like to learn?", placeholder="Why is 'went' the past tense of 'go'?")
if st.button("Ask tutor", use_container_width=True):
    if not question.strip(): st.warning("Write a question first.")
    else:
        with st.spinner("Preparing an explanation..."):
            answer = ask_ai(question, "You are a patient linguistics tutor. Be concise, accurate and use examples.")
        if answer: st.markdown(answer)
        else: st.info("AI Tutor is not configured. Add a provider key privately in Streamlit secrets; the rest of Words works without it.")
