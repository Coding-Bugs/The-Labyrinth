from sys import stderr

class Search:
    def __init__(self, Q, V, board):
        self.reached = Q
        self.frontier = V
        self.gameboard = board
    
    def printTNode(self, node):
        f = node.f
        g = node.g
        h = node.h
        row = node.state[0]
        col = node.state[1]
        p = node.parent
        print(f"F: {f}, G: {g}, H: {h}, S: ({row}, {col}), P: {p}", file=stderr, flush=True)
    
    # yields all adjacent valid tiles 
    def successors(self, row, col):
        # Up
        if row > 0:
            yield (row - 1, col)

        # Right
        if col < self.gameboard.width - 1:
            yield (row, col + 1)

        # Down
        if row < self.gameboard.height - 1:
            yield (row + 1, col)

        # Left
        if col > 0:
            yield (row, col - 1)