from sys import stderr
from collections import deque

from state import State

class Game:
    def __init__(self, board, verbose=False):
        self.state = State.EXPLORE
        self.gameboard = board
        self.moves = deque()
        self.verbose = verbose

    def addMoves(self, queue: deque):
        self.moves += queue

    def nextMove(self):
        return self.moves.popleft()

    def updateState(self, state):
        self.state = state
    
    def printError(self, target):
        if self.verbose:
            print(target, file=stderr, flush=True)