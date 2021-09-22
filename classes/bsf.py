from sys import stderr
from collections import deque

from search import Search

class BFS(Search):
    def __init__(self, board, v=False):
        super().__init__(deque(), set(), board)
        self.full = False
        self.verbose = v

    def checkFull(self):
        self.search((self.gameboard.start.x, self.gameboard.start.y), "?")
        return self.full

    def printError(self, target):
        print(target, file=stderr, flush=True)

    def search(self, start: tuple, target: str):

        # Initialize queue and visited set
        self.frontier = deque()
        self.reached = set()

        # Prep for search
        node = self.gameboard.board[start[0]][start[1]]
        self.frontier.append(node)
        self.reached.add(node)

        # Walk search
        while self.frontier:
            vertex = self.frontier.popleft()
            if self.verbose:
                self.printError("Current Row: " + str(vertex.x) + ", Current Col: " + str(vertex.y))

            # Check Target Condition
            if vertex.ch == target:
                return (vertex.x, vertex.y)

            # Check successors
            for pos in self.successors(vertex.x, vertex.y):
                n = self.gameboard.board[pos[0]][pos[1]]
                if n.ch == target:
                    if target == "?":
                        self.full = False
                        return (vertex.x, vertex.y)
                    else:
                        return (n.x, n.y)
                if n.ch != "#" and n.ch != '?' and n not in self.reached:
                    if self.verbose:
                        self.printError("Adding (" + str(n.x) + ", " + str(n.y) + "): " + str(n.ch) + " to Frontier")
                    self.frontier.append(n)
                    self.reached.add(n)
                if n.ch == "?":
                    self.full = False
            if self.verbose:
                self.printError("")
        self.full = True
        return None