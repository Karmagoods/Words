import streamlit as st
import pandas as pd

from services.spacy_service import (
    analyze_text,
    get_tokens,
    get_dependencies,
    get_entities,
    get_summary
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Sentence Analyzer",
    page_icon="🧠",
    layout="wide"
)

# ==========================================================
# HEADER
# ==========================================================

st.title("🧠 Sentence Analyzer")

st.write(
    """
Analyze the grammar and linguistic structure of complete
sentences using Natural Language Processing.
    """
)

st.divider()

# ==========================================================
# INPUT
# ==========================================================

sentence = st.text_area(
    "Enter a sentence",
    height=140,
    placeholder="Example:\nThe quick brown fox jumps over the lazy dog."
)

analyze = st.button(
    "Analyze Sentence",
    use_container_width=True
)

# ==========================================================
# ANALYSIS
# ==========================================================

if analyze:

    if not sentence.strip():

        st.warning("Please enter a sentence.")

        st.stop()

    doc = analyze_text(sentence)

    summary = get_summary(sentence)

    tokens = get_tokens(doc)

    dependencies = get_dependencies(doc)

    entities = get_entities(doc)

    # ------------------------------------------------------
    # METRICS
    # ------------------------------------------------------

    st.subheader("📊 Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric("Tokens", summary["tokens"])
    c2.metric("Sentences", summary["sentences"])
    c3.metric("Entities", summary["entities"])

    st.divider()

    # ------------------------------------------------------
    # TOKENS
    # ------------------------------------------------------

    st.subheader("📝 Token Analysis")

    st.dataframe(
        pd.DataFrame(tokens),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ------------------------------------------------------
    # DEPENDENCIES
    # ------------------------------------------------------

    st.subheader("🔗 Dependency Parsing")

    st.dataframe(
        pd.DataFrame(dependencies),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ------------------------------------------------------
    # ENTITIES
    # ------------------------------------------------------

    st.subheader("🏷 Named Entities")

    if entities:

        st.dataframe(
            pd.DataFrame(entities),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No named entities detected.")

    st.divider()

    # ------------------------------------------------------
    # TOKEN DETAILS
    # ------------------------------------------------------

    st.subheader("🔍 Individual Word Analysis")

    for token in tokens:

        with st.expander(token["text"]):

            st.write(f"**Lemma:** {token['lemma']}")
            st.write(f"**Part of Speech:** {token['pos']}")
            st.write(f"**Grammar Tag:** {token['tag']}")
            st.write(f"**Dependency:** {token['dependency']}")
            st.write(f"**Head Word:** {token['head']}")
            st.write(f"**Morphology:** {token['morphology']}")

    st.divider()

    # ------------------------------------------------------
    # COMING SOON
    # ------------------------------------------------------

    st.subheader("🚀 Coming Soon")

    st.info("""
• Constituency Parse Trees

• Syntax Tree Visualisation

• Grammar Checking

• Sentence Complexity Score

• Readability Analysis

• Semantic Role Labelling

• AI Explanation

• Translation

• Voice Analysis
""")

else:

    st.info(
        "Enter a sentence above and click **Analyze Sentence**."
    )

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.header("Sentence Tools")

    st.success("✔ Tokenization")
    st.success("✔ POS Tagging")
    st.success("✔ Dependencies")
    st.success("✔ Named Entities")

    st.divider()

    st.write("Planned")

    st.checkbox("Syntax Tree", disabled=True)
    st.checkbox("Grammar Correction", disabled=True)
    st.checkbox("Semantic Roles", disabled=True)
    st.checkbox("AI Tutor", disabled=True)