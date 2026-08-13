import streamlit as st
from games.base_game import choose_words
from games.wordsearch import make_grid, find_word
from utils.session import get, put, record_win

st.set_page_config(page_title="Word Search | Words", page_icon="🔎", layout="centered")
st.title("🔎 Word Search")
if st.button("New puzzle", use_container_width=True) or not get("wordsearch"):
    words = choose_words(count=6, minimum=4, maximum=10, random_category=True)
    grid, positions = make_grid(words, 10)
    put("wordsearch", {"words": list(positions), "grid": grid, "found": set()})
puzzle = get("wordsearch")
st.caption("Enter the coordinates for the first and last letter. Rows and columns start at 1.")
st.code("\n".join(" ".join(row) for row in puzzle["grid"]), language=None)
st.write("Find: " + ", ".join(f"~~{word}~~" if word in puzzle["found"] else word for word in puzzle["words"]))
c1, c2, c3, c4 = st.columns(4)
row1 = c1.number_input("Start row", 1, 10, 1); col1 = c2.number_input("Start column", 1, 10, 1)
row2 = c3.number_input("End row", 1, 10, 1); col2 = c4.number_input("End column", 1, 10, 1)
if st.button("Check selection", use_container_width=True):
    matched = next((word for word in puzzle["words"] if word not in puzzle["found"] and find_word(puzzle["grid"], word, row1-1, col1-1, row2-1, col2-1)), None)
    if matched:
        puzzle["found"].add(matched); put("wordsearch", puzzle); st.success(f"Found **{matched}**!")
        if len(puzzle["found"]) == len(puzzle["words"]): record_win(50); st.balloons()
    else: st.warning("That selection does not match a remaining word.")