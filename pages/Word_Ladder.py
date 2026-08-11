import streamlit as st
from games.ladder import LADDERS, validate_step
from utils.session import get, put, record_win

st.set_page_config(page_title="Word Ladder | Words", page_icon="🪜", layout="centered")
st.title("🪜 Word Ladder")
if st.button("New ladder", use_container_width=True) or not get("ladder"):
    puzzle = LADDERS[0 if get("ladder_index", -1) == 1 else 1]; put("ladder_index", 0 if get("ladder_index", -1) == 1 else 1); put("ladder", puzzle); put("ladder_steps", [puzzle[0]]); put("ladder_done", False)
start, target, allowed = get("ladder")
steps = get("ladder_steps")
st.write(f"Change one letter at a time: **{start.upper()}** → **{target.upper()}**")
st.write(" → ".join(word.upper() for word in steps))
candidate = st.text_input("Next word", max_chars=len(start), disabled=get("ladder_done", False))
if st.button("Add step", use_container_width=True) and not get("ladder_done", False):
    valid, message = validate_step(steps[-1], candidate, allowed)
    if valid:
        steps.append(candidate.lower()); put("ladder_steps", steps)
        if steps[-1] == target: put("ladder_done", True); record_win(max(10, 35-len(steps)*3)); st.success("Ladder complete!")
        else: st.success(message)
    else: st.warning(message)
