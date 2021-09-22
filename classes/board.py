from sys import stderr

from slot import Slot
from pos import Pos

class Board():
    def __init__(self, width: int, height: int):
        # Constants
        self.width = width
        self.height = height

        self.board = [[Slot(x, y, "?") for y in range(width)] for x in range(height)]
        self.start = None
        self.control = None

    # Prints board to Standard Error
    def printBoard(self):
        # Print each row
        for x in range(self.height):
            print("[", file=stderr, flush=True, end="")

            # Print each column
            for y in range(self.width):
                print(self.board[x][y].ch, file=stderr, flush=True, end="")

                if y != self.width - 1:
                    print(f", ", file=stderr, flush=True, end="")

            print("]", file=stderr, flush=True)

    # Updates 1 entire row of the board
    def updateRow(self, x: int, row: str):
        y = 0
        for letter in row:
            if letter == "T":
                self.start = Pos(x, y)
            elif letter == "C":
                self.control = Pos(x, y)
            self.board[x][y].update(letter)
            y += 1