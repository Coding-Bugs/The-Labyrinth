from sys import stderr

from pos import Pos

class Slot (Pos):
    def __init__(self, x, y, ch):
        super().__init__(x, y)
        self.ch = ch

    def print(self):
        print(f"X: {self.x}, Y: {self.y}, Ch: {self.ch}", file=stderr, flush=True)

    def update(self, ch: str):
        self.ch = ch