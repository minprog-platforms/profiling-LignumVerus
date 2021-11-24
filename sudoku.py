"""
- sudoku.py
- Finn Peranovic

- Creates a Sudoku class that is used to solve a sudoku in solve.py.
"""
from __future__ import annotations
from typing import Iterable


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid: list[list[int]] = []

        for puzzle_row in puzzle:
            row = []

            for element in puzzle_row:
                row.append(element)

            self._grid.append(row)

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        self._grid[y][x] = value

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        self._grid[y][x] = 0

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y (used for pytest testing)."""
        value = self._grid[y][x]

        return value

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        all_options = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        options = set()

        # Get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        # get all possible values
        row_values = self.row_values(y)
        column_values = self.column_values(x)
        block_values = self.block_values(block_index)

        for value in all_options:
            if value not in row_values and value not in column_values and value not in block_values:
                options.add(value)

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        next_x, next_y = -1, -1

        for y in range(9):
            for x in range(9):
                if self._grid[y][x] == 0:
                    next_x, next_y = x, y

                    # added return
                    return next_x, next_y

        return next_x, next_y

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""
        values = self._grid[i]

        return values

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""
        values = []

        for j in range(9):
            values.append(self._grid[j][i])

        return values

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        values = []

        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        for x in range(x_start, x_start + 3):
            for y in range(y_start, y_start + 3):
                values.append(self._grid[y][x])

        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        values = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        result = True

        for i in range(9):
            for j in range(9):
                if self._grid[j][i] not in values:
                    result = False

                    return result

        return result

    def __str__(self) -> str:
        representation = ""

        for row in self._grid:
            representation += " ".join(map(str, row)) + "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[list[int]] = []

    with open(filename) as f:
        for raw_line in f:

            # add lines as lists of integers to puzzle
            line = raw_line.strip().split(",")
            new_line = [int(x) for x in line]

            puzzle.append(new_line)

    return Sudoku(puzzle)
