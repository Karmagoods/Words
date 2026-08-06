import json
import streamlit as st

from services.spacy_service import (
    analyze_text,
    get_tokens,
    get_summary,
)

from services.dictionary import summarize


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Word Explorer",
    page_icon="🔎",
    layout="wide",
)

# ==========================================================
# HEADER
# ==========================================================

st.title("🔎 Word Explorer")

st.write(
    "Explore the meaning, structure, pronunciation, grammar and linguistic "
    "properties of any word or phrase."
)

st.caption(
    "Examples: *understanding*, *photosynthesis*, *run*, "
    "*artificial intelligence*, *to be or not to be*"
)

st.divider()

# ==========================================================
# SEARCH
# ==========================================================

search = st.text_input(
    "Enter a word or phrase",
    placeholder="Example: understanding",
)

analyze = st.button(
    "Analyze",
    use_container_width=True,
)

# ==========================================================
# RESULTS
# ==========================================================

if analyze:

    if not search.strip():
        st.warning("Please enter a word or phrase.")
        st.stop()

    with st.spinner("Analyzing language..."):

        doc = analyze_text(search)

        tokens = get_tokens(doc)

        summary = get_summary(search)

        try:
            dictionary = summarize(search)
        except Exception:
            dictionary = None

    st.success(f'Analysis completed for **"{search}"**')

    # ------------------------------------------------------

    m1, m2, m3 = st.columns(3)

    m1.metric("Tokens", summary["tokens"])
    m2.metric("Sentences", summary["sentences"])
    m3.metric("Named Entities", summary["entities"])

    st.divider()

    col1, col2 = st.columns(2)

    # ======================================================
    # LEFT COLUMN
    # ======================================================

    with col1:

        with st.expander("📖 Definitions", expanded=True):

            if dictionary and dictionary.get("definitions"):

                for i, definition in enumerate(
                    dictionary["definitions"], start=1
                ):

                    st.markdown(
                        f"""
**{i}. {definition["part_of_speech"]}**

{definition["definition"]}
"""
                    )

            else:
                st.info("No definitions available.")

        with st.expander("🧩 Morphology", expanded=True):

            for token in tokens:

                st.markdown(
                    f"""
### {token["text"]}

- **Lemma:** `{token["lemma"]}`
- **Morphology:** `{token["morphology"]}`
"""
                )

        with st.expander("🏷 Parts of Speech"):

            for token in tokens:

                st.write(
                    f"**{token['text']}** → {token['pos']}"
                )

        with st.expander("🔄 Synonyms"):

            if dictionary and dictionary.get("synonyms"):

                st.write(", ".join(dictionary["synonyms"]))

            else:
                st.info("No synonyms available.")

        with st.expander("⛔ Antonyms"):

            if dictionary and dictionary.get("antonyms"):

                st.write(", ".join(dictionary["antonyms"]))

            else:
                st.info("No antonyms available.")

    # ======================================================
    # RIGHT COLUMN
    # ======================================================

    with col2:

        with st.expander("🔊 Pronunciation", expanded=True):

            if dictionary:

                ipa = dictionary.get("ipa")

                audio = dictionary.get("audio")

                if ipa:
                    st.write(f"### IPA\n`{ipa}`")

                if audio:
                    st.audio(audio)

                if not ipa and not audio:
                    st.info("No pronunciation available.")

            else:
                st.info("No pronunciation available.")

        with st.expander("📚 Example Sentences", expanded=True):

            found = False

            if dictionary:

                for definition in dictionary.get("definitions", []):

                    example = definition.get("example")

                    if example:

                        found = True

                        st.markdown(f"> {example}")

            if not found:
                st.info("No example sentences available.")

        with st.expander("🔍 Token Details"):

            st.dataframe(
                tokens,
                use_container_width=True,
                hide_index=True,
            )

        with st.expander("🌍 Etymology"):

            st.info(
                "Etymology integration will connect to "
                "Etymonline, Wiktionary and AI-generated historical analysis."
            )

        with st.expander("⬇ Export"):

            export = {
                "query": search,
                "summary": summary,
                "dictionary": dictionary,
                "tokens": tokens,
            }

            st.download_button(
                "Download Analysis (JSON)",
                json.dumps(export, indent=4),
                file_name=f"{search}.json",
                mime="application/json",
                use_container_width=True,
            )

# ==========================================================
# EMPTY STATE
# ==========================================================

else:

    st.info(
        "👆 Enter a word or phrase above and click **Analyze**."
    )

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.header("🔎 Word Explorer")

    st.success("✔ Definitions")
    st.success("✔ Morphology")
    st.success("✔ Parts of Speech")
    st.success("✔ Synonyms")
    st.success("✔ Antonyms")
    st.success("✔ IPA Pronunciation")
    st.success("✔ Example Sentences")
    st.success("✔ JSON Export")

    st.divider()

    st.subheader("Coming Soon")

    st.checkbox("AI Etymology", value=False, disabled=True)
    st.checkbox("Word Family", value=False, disabled=True)
    st.checkbox("Cognates", value=False, disabled=True)
    st.checkbox("Semantic Graph", value=False, disabled=True)
    st.checkbox("Syntax Tree", value=False, disabled=True)
    st.checkbox("Language Detection", value=False, disabled=True)
    st.checkbox("Translation", value=False, disabled=True)
    st.checkbox("AI Tutor", value=False, disabled=True)
