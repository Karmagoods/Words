import json
import streamlit as st
from services.word_engine import WordEngine

st.set_page_config(page_title="Word Explorer | Words", page_icon="🔎", layout="wide")
st.title("🔎 Word Explorer")
st.caption("Definitions, pronunciation, morphology, word relationships and etymology in one place.")
query = st.text_input("Enter a word or phrase", placeholder="understanding")
if st.button("Analyze", use_container_width=True):
    if not query.strip(): st.warning("Please enter a word or phrase.")
    else:
        with st.spinner("Analyzing language..."): result = WordEngine().search(query)
        st.success(f"Analysis for **{query.strip()}**")
        summary, tokens = result.get("statistics", {}), result.get("tokens", [])
        c1, c2, c3 = st.columns(3); c1.metric("Tokens", summary.get("tokens", len(tokens))); c2.metric("Sentences", summary.get("sentences", 0)); c3.metric("Entities", summary.get("entities", 0))
        left, right = st.columns(2)
        with left:
            with st.expander("📖 Definitions", expanded=True):
                definitions = result.get("definitions", [])
                if definitions:
                    for item in definitions[:8]:
                        st.write(f"**{item.get('part_of_speech', '')}** — {item.get('definition', '')}")
                        if item.get("example"): st.caption(f"Example: {item['example']}")
                else: st.info("No dictionary definition was returned.")
            with st.expander("🧩 Morphology and NLP", expanded=True):
                if tokens: st.dataframe(tokens, use_container_width=True, hide_index=True)
                else: st.info("NLP details are unavailable.")
            with st.expander("🔁 Synonyms and antonyms"): st.write("**Synonyms:** " + ", ".join(result.get("synonyms", [])[:25]) + "\n\n**Antonyms:** " + ", ".join(result.get("antonyms", [])[:25]))
        with right:
            with st.expander("🔊 Pronunciation", expanded=True):
                if result.get("ipa"): st.code(result["ipa"])
                if result.get("audio"): st.audio(result["audio"])
                if not result.get("ipa") and not result.get("audio"): st.info("No pronunciation audio or IPA is available.")
            with st.expander("🕸 Word discovery", expanded=True):
                for label, key in [("Related", "related"), ("Rhymes", "rhymes"), ("Sounds like", "sounds_like")]: st.write(f"**{label}:** " + ", ".join(result.get(key, [])[:20]))
            with st.expander("🌍 Etymology"): st.write(result.get("etymology") or "No etymology was returned by the available source.")
            st.download_button("Download analysis (JSON)", json.dumps(result, indent=2, default=str), file_name=f"{query.strip().replace(' ', '_')}_analysis.json", mime="application/json", use_container_width=True)
else: st.info("Enter a word or phrase and choose Analyze.")
