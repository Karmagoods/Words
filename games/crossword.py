from __future__ import annotations
from games.base_game import clean_word


def make_clues(words_with_clues):
    """Return a compact fill-in crossword model; UI presents one clue per row."""
    return [{"number": index, "answer": clean_word(answer), "clue": clue} for index, (answer, clue) in enumerate(words_with_clues, 1) if clean_word(answer)]


def check_answers(clues, answers):
    correct = [clue["number"] for clue in clues if clean_word(answers.get(str(clue["number"]), "")) == clue["answer"]]
    return correct, len(correct) == len(clues)


DEFAULT_CLUES = make_clues([("language", "A system of communication using words"), ("synonym", "A word with a similar meaning"), ("verb", "A word that usually expresses an action"), ("rhyme", "Words with matching end sounds")])
