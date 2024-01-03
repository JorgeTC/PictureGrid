from dataclasses import dataclass


@dataclass
class Position:
    row: int
    column: int


class IterGrid:
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns

    @property
    def diagonals(self):
        return self.rows + self.columns - 1

    def iterate_diagonals(self):

        for d in range(self.diagonals):
            end_row = max(0, d - self.columns + 1)
            start_row = min(d, self.rows - 1)

            for row in range(start_row, end_row - 1, -1):
                col = d - row
                yield Position(row, col)

    def diagonal_length(self, diagonal: int) -> int:
        if diagonal not in range(self.diagonals):
            raise ValueError

        end_row = max(0, diagonal - self.columns + 1)
        start_row = min(diagonal, self.rows - 1)
        return start_row - end_row + 1
