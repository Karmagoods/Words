from games.hangman import HangmanGame
from games.unscramble import is_correct
from games.ladder import one_letter_apart
from games.wordsearch import make_grid, find_word
from games.crossword import make_clues, check_answers
from games.spelling_bee import valid_bee_word


def test_hangman_win_and_miss():
    game = HangmanGame("cat", 2)
    assert game.guess("x")["correct"] is False
    for letter in "cat": game.guess(letter)
    assert game.won and game.masked_word == "c a t"


def test_word_games_helpers():
    assert is_correct("Language", "language")
    assert one_letter_apart("cold", "cord")
    assert valid_bee_word("angle", "aelngru", "a")
    grid, placed = make_grid(["river"], 8, seed=7)
    row, col, end_row, end_col = placed["river"]
    assert find_word(grid, "river", row, col, end_row, end_col)


def test_crossword_answers():
    clues = make_clues([("verb", "action word")])
    assert check_answers(clues, {"1": "verb"}) == ([1], True)
