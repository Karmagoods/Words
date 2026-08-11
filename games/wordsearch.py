from __future__ import annotations
import random
from games.base_game import normalise_words

DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))


def make_grid(words, size=10, seed=None):
    rng = random.Random(seed)
    words = sorted(normalise_words(words), key=len, reverse=True)
    grid = [["" for _ in range(size)] for _ in range(size)]
    placed = {}
    for word in words:
        options = []
        for _ in range(100):
            dr, dc = rng.choice(DIRECTIONS); row, col = rng.randrange(size), rng.randrange(size)
            end_r, end_c = row + dr * (len(word) - 1), col + dc * (len(word) - 1)
            if not (0 <= end_r < size and 0 <= end_c < size): continue
            if all(not grid[row + dr*i][col + dc*i] or grid[row + dr*i][col + dc*i] == char for i, char in enumerate(word)):
                options.append((row, col, dr, dc)); break
        if not options: continue
        row, col, dr, dc = options[0]
        for i, char in enumerate(word): grid[row + dr*i][col + dc*i] = char.upper()
        placed[word] = (row, col, row + dr*(len(word)-1), col + dc*(len(word)-1))
    for row in grid:
        for index, char in enumerate(row):
            if not char: row[index] = rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return grid, placed


def find_word(grid, word, start_row, start_col, end_row, end_col):
    word = word.upper(); size = len(grid)
    if not word or not all(0 <= v < size for v in (start_row, start_col, end_row, end_col)): return False
    length = max(abs(end_row-start_row), abs(end_col-start_col)) + 1
    if length != len(word): return False
    dr = 0 if end_row == start_row else (1 if end_row > start_row else -1)
    dc = 0 if end_col == start_col else (1 if end_col > start_col else -1)
    if dr and dc and abs(end_row-start_row) != abs(end_col-start_col): return False
    return "".join(grid[start_row+dr*i][start_col+dc*i] for i in range(length)) in (word, word[::-1])
