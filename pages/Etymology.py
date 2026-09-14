import streamlit as st
from services.etymology import analyze


st.set_page_config(
    page_title="Etymology | Words",
    page_icon="🌍",
    layout="wide",
)


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

st.title("🌍 Etymology Explorer")
st.caption(
    "Trace a word through languages, historical forms, related words, "
    "and external etymology sources."
)


# ---------------------------------------------------------
# SEARCH
# ---------------------------------------------------------

word = st.text_input(
    "Enter a word",
    placeholder="e.g. felicity, philosophy, democracy, language",
)


explore = st.button(
    "Explore origins",
    type="primary",
    use_container_width=True,
)


# ---------------------------------------------------------
# EMPTY STATE
# ---------------------------------------------------------

if not explore:
    st.info(
        "Enter a word above and explore where it came from, "
        "how its meaning developed, and which words are related to it."
    )

    st.markdown("### What you can explore")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Historical journey**")
        st.caption(
            "See known stages of a word's development across languages "
            "and periods."
        )

    with col2:
        st.markdown("**Word relationships**")
        st.caption(
            "Explore cognates, related words, and possible language-family "
            "connections."
        )

    with col3:
        st.markdown("**External sources**")
        st.caption(
            "Jump to established reference sources such as Wiktionary "
            "and Etymonline."
        )

    st.stop()


# ---------------------------------------------------------
# VALIDATE INPUT
# ---------------------------------------------------------

clean_word = word.strip()

if not clean_word:
    st.warning("Please enter a word.")
    st.stop()


# ---------------------------------------------------------
# ANALYZE
# ---------------------------------------------------------

with st.spinner(f"Tracing the history of “{clean_word}”..."):
    result = analyze(clean_word)


# ---------------------------------------------------------
# RESULT HEADER
# ---------------------------------------------------------

st.divider()

st.subheader(f"“{clean_word}”")

source = result.get("source")

if source:
    st.caption(f"Primary data source: {source}")
else:
    st.caption("No structured primary source was available.")


# ---------------------------------------------------------
# MAIN CONTENT
# ---------------------------------------------------------

left, right = st.columns([2.2, 1], gap="large")


# =========================================================
# LEFT COLUMN
# =========================================================

with left:

    # -----------------------------------------------------
    # WORD HISTORY
    # -----------------------------------------------------

    st.markdown("### Word history")

    history = (
        result.get("history")
        or result.get("summary")
        or ""
    ).strip()

    if history:
        st.write(history)
    else:
        st.info(
            "No structured etymology was found in the primary source."
        )

        if result.get("source") == "Wiktionary":
            st.caption(
                "A Wiktionary entry exists for this word, but a detailed "
                "historical explanation was not extracted automatically."
            )
        else:
            st.caption(
                "You can use the external references on the right "
                "to investigate the word further."
            )


    # -----------------------------------------------------
    # TIMELINE
    # -----------------------------------------------------

    timeline = result.get("timeline", [])

    st.markdown("### Historical timeline")

    if timeline:

        for stage in timeline:
            period = stage.get("period") or "Historical stage"
            language = stage.get("language") or "Unknown language"
            historical_word = stage.get("word") or ""

            with st.container(border=True):
                st.markdown(f"**{period}**")

                if historical_word:
                    st.markdown(
                        f"### {historical_word}"
                    )

                st.caption(language)

    else:
        st.info(
            "No structured timeline is available for this word yet."
        )


    # -----------------------------------------------------
    # RELATED WORDS
    # -----------------------------------------------------

    related_words = result.get("related_words", [])

    st.markdown("### Related words")

    if related_words:
        st.write(" · ".join(related_words))
    else:
        st.caption("No related words were found.")


# =========================================================
# RIGHT COLUMN
# =========================================================

with right:

    # -----------------------------------------------------
    # LANGUAGE INFORMATION
    # -----------------------------------------------------

    st.markdown("### Language")

    language = result.get("language")
    family = result.get("family")

    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.metric(
            "Root language",
            language or "Unknown",
        )

    with info_col2:
        st.metric(
            "Family",
            family or "Unknown",
        )


    # -----------------------------------------------------
    # COGNATES
    # -----------------------------------------------------

    st.markdown("### Cognates")

    cognates = result.get("cognates", [])

    if cognates:
        for cognate in cognates:
            st.markdown(f"- {cognate}")
    else:
        st.caption("No cognates found.")


    # -----------------------------------------------------
    # SOURCES
    # -----------------------------------------------------

    st.markdown("### Sources")

    source_url = result.get("source_url")
    etymonline_url = result.get("etymonline_url")

    if source_url:

        source_name = source or "Primary source"

        st.link_button(
            f"Open {source_name}",
            source_url,
            use_container_width=True,
        )

    if etymonline_url:

        st.link_button(
            "Explore on Etymonline",
            etymonline_url,
            use_container_width=True,
        )

        st.caption(
            "External reference — Etymonline data is not directly "
            "retrieved by this app."
        )


# ---------------------------------------------------------
# FOOTER / STATUS
# ---------------------------------------------------------

st.divider()

if source == "Wordnik":
    st.caption(
        "Wordnik supplied the primary result. Additional historical "
        "research may be available through the external references."
    )

elif source == "Wiktionary":
    st.caption(
        "Wordnik did not provide structured etymology for this word, "
        "so the app used Wiktionary as a fallback."
    )

else:
    st.caption(
        "No structured etymology was found. External references may "
        "still provide useful historical information."
    )