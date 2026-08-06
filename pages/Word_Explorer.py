import streamlit as st

from services.spacy_service import (
    analyze_text,
    get_tokens,
    get_summary
)

from services.dictionary import (
    summarize
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Word Explorer",
    page_icon="🔎",
    layout="wide"
)

# ==========================================================
# HEADER
# ==========================================================

st.title("🔎 Word Explorer")

st.write(
    "Explore the meaning, structure, history and linguistic properties "
    "of any word or phrase."
)

st.divider()

# ==========================================================
# SEARCH
# ==========================================================

search = st.text_input(
    "Enter a word or phrase",
    placeholder="Example: understanding"
)

analyze = st.button(
    "Analyze",
    use_container_width=True
)

# ==========================================================
# RESULTS
# ==========================================================

if analyze:

    if not search.strip():

        st.warning("Please enter a word or phrase.")
        st.stop()

    # --------------------------------------
    # Analyse
    # --------------------------------------

    doc = analyze_text(search)

    tokens = get_tokens(doc)

    summary = get_summary(search)

    dictionary = summarize(search)

    st.success(f'Analyzing "{search}"')

    col1, col2 = st.columns(2)

    # ======================================================
    # LEFT COLUMN
    # ======================================================

    with col1:

        with st.container(border=True):

            st.subheader("📖 Definitions")

            if dictionary:

                for i, definition in enumerate(dictionary["definitions"], start=1):

                    st.markdown(
                        f"**{i}. ({definition['part_of_speech']})** "
                        f"{definition['definition']}"
                    )

            else:

                st.info("No dictionary definition found.")

        with st.container(border=True):

            st.subheader("🧩 Morphology")

            for token in tokens:

                st.markdown(
                    f"""
**{token['text']}**

- Lemma: `{token['lemma']}`
- Morphology: `{token['morphology']}`
"""
                )

        with st.container(border=True):

            st.subheader("🏷 Part of Speech")

            for token in tokens:

                st.write(
                    f"**{token['text']}** → {token['pos']}"
                )

        with st.container(border=True):

            st.subheader("🔄 Synonyms")

            if dictionary and dictionary["synonyms"]:

                st.write(", ".join(dictionary["synonyms"]))

            else:

                st.info("No synonyms available.")

        with st.container(border=True):

            st.subheader("⛔ Antonyms")

            if dictionary and dictionary["antonyms"]:

                st.write(", ".join(dictionary["antonyms"]))

            else:

                st.info("No antonyms available.")

    # ======================================================
    # RIGHT COLUMN
    # ======================================================

    with col2:

        with st.container(border=True):

            st.subheader("🔊 Pronunciation")

            if dictionary:

                if dictionary["ipa"]:

                    st.write(f"**IPA:** {dictionary['ipa']}")

                if dictionary["audio"]:

                    st.audio(dictionary["audio"])

            else:

                st.info("No pronunciation available.")

        with st.container(border=True):

            st.subheader("📚 Example Sentences")

            if dictionary:

                found = False

                for definition in dictionary["definitions"]:

                    if definition["example"]:

                        found = True

                        st.markdown(
                            f"> {definition['example']}"
                        )

                if not found:

                    st.info("No example sentences available.")

            else:

                st.info("No examples available.")

        with st.container(border=True):

            st.subheader("📊 Word Statistics")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Tokens",
                summary["tokens"]
            )

            c2.metric(
                "Sentences",
                summary["sentences"]
            )

            c3.metric(
                "Entities",
                summary["entities"]
            )

        with st.container(border=True):

            st.subheader("🔍 Token Details")

            st.dataframe(
                tokens,
                use_container_width=True,
                hide_index=True
            )

        with st.container(border=True):

            st.subheader("🌍 Etymology")

            st.info("Coming in the next version.")

# ==========================================================
# EMPTY STATE
# ==========================================================

else:

    st.info(
        "👆 Enter a word or phrase above and click Analyze."
    )

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.header("Explorer")

    st.write("Current Features")

    st.success("✔ Definitions")
    st.success("✔ Morphology")
    st.success("✔ Parts of Speech")
    st.success("✔ Synonyms")
    st.success("✔ Antonyms")
    st.success("✔ IPA Pronunciation")
    st.success("✔ Example Sentences")

    st.divider()

    st.write("Coming Soon")

    st.checkbox("Etymology", value=False, disabled=True)
    st.checkbox("Word Family", value=False, disabled=True)
    st.checkbox("Semantic Graph", value=False, disabled=True)
    st.checkbox("Syntax Tree", value=False, disabled=True)
    st.checkbox("AI Tutor", value=False, disabled=True)