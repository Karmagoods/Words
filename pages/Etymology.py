import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Etymology Explorer",
    page_icon="🌍",
    layout="wide"
)

# ==========================================================
# HEADER
# ==========================================================

st.title("🌍 Etymology Explorer")

st.write(
    """
Discover the origins and historical journey of words through
time and across languages.
    """
)

st.divider()

# ==========================================================
# SEARCH
# ==========================================================

word = st.text_input(
    "Enter a word",
    placeholder="Example: language"
)

search = st.button(
    "Explore Origins",
    use_container_width=True
)

# ==========================================================
# RESULTS
# ==========================================================

if search:

    if not word.strip():

        st.warning("Please enter a word.")

        st.stop()

    st.success(f'Looking up the origins of "{word}"')

    col1, col2 = st.columns([2, 1])

    # ------------------------------------------------------
    # LEFT
    # ------------------------------------------------------

    with col1:

        with st.container(border=True):

            st.subheader("📜 Word History")

            st.info(
                "Etymology service coming soon.\n\n"
                "This section will explain where the word originated and "
                "how its meaning evolved over time."
            )

        with st.container(border=True):

            st.subheader("🕰 Timeline")

            timeline = [
                "Proto Language",
                "Ancient Language",
                "Medieval Language",
                "Early Modern English",
                "Modern English"
            ]

            for stage in timeline:
                st.write(f"⬇ {stage}")

        with st.container(border=True):

            st.subheader("🌳 Word Family")

            st.write("Coming soon")

        with st.container(border=True):

            st.subheader("🌍 Cognates")

            st.write("Coming soon")

    # ------------------------------------------------------
    # RIGHT
    # ------------------------------------------------------

    with col2:

        with st.container(border=True):

            st.subheader("📊 Origin")

            st.metric("Estimated Age", "Unknown")
            st.metric("Language Family", "Unknown")
            st.metric("Root Language", "Unknown")

        with st.container(border=True):

            st.subheader("📚 Related Words")

            st.write("Coming soon")

        with st.container(border=True):

            st.subheader("🔗 Borrowed Into")

            st.write("Coming soon")

        with st.container(border=True):

            st.subheader("🤖 AI Summary")

            st.info(
                "AI-generated explanations of a word's historical "
                "development will appear here."
            )

else:

    st.info(
        "Enter a word above to explore its history."
    )

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.header("Etymology")

    st.success("✓ Timeline")
    st.success("✓ History")

    st.divider()

    st.write("Planned")

    st.checkbox("Historical Maps", disabled=True)
    st.checkbox("Language Tree", disabled=True)
    st.checkbox("Word Evolution", disabled=True)
    st.checkbox("Pronunciation Changes", disabled=True)
    st.checkbox("Borrowed Words", disabled=True)