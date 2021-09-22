from sys import stderr

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print(self):
        print(f"X: {self.x}, Y: {self.y}", file=stderr, flush=True)