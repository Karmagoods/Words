"""Namespaced Streamlit session helpers."""
from __future__ import annotations
import streamlit as st


def get(key, default=None):
    return st.session_state.get(key, default)


def put(key, value):
    st.session_state[key] = value
    return value


def reset(key):
    st.session_state.pop(key, None)


def stats():
    return st.session_state.setdefault("words_stats", {"score": 0, "wins": 0, "no_hint_wins": 0, "daily_wins": 0})


def record_win(points: int, used_hint=False, daily=False):
    data = stats(); data["score"] += points; data["wins"] += 1
    if not used_hint: data["no_hint_wins"] += 1
    if daily: data["daily_wins"] += 1
    return data
