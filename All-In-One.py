from sys import stderr
from collections import deque, namedtuple
from heapq import heappush, heappop
import enum


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print(self):
        print(f"X: {self.x}, Y: {self.y}", file=stderr, flush=True)

class Slot (Pos):
    def __init__(self, x, y, ch):
        super().__init__(x, y)
        self.ch = ch

    def print(self):
        print(f"X: {self.x}, Y: {self.y}, Ch: {self.ch}",
              file=stderr, flush=True)

    def update(self, ch: str):
        self.ch = ch

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


class State (enum.Enum):
    EXPLORE = 1
    CONTROL = 2
    ESCAPE = 3


    # A Star node
TNode = namedtuple('TNode', ['f', 'g', 'h', 'state', 'parent'])

class Search:

    def __init__(self, Q, V, board: Board):
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

class AStar (Search):

    def __init__(self, board: Board, alarm: int, v=False):
        super().__init__({}, [], board)
        self.alarm = alarm
        self.verbose = v

    def heuristic(self, cords: tuple, target: tuple):
        # Returns the distance vertically and horizontally between two points summed together
        return abs(target[1] - cords[1]) + abs(target[0] - cords[0])

    def is_goal(self, node: tuple, target: tuple):
        # Check if row and col of node matches with the target's
        if node[0] == target[0] and node[1] == target[1]:
            return True
        return False

    def getPath(self, treenode: TNode):

        stack = []
        node = treenode

        # Walk parent path adding movement commands to a stack
        while node and node.parent:
            parent = node.parent

            if self.verbose:
                self.printTNode(node)
                self.printTNode(parent)

            # Right from parent
            if parent.state[1] + 1 == node.state[1]:
                stack.append("RIGHT")
            # Left from parent
            elif parent.state[1] - 1 == node.state[1]:
                stack.append("LEFT")
            # Down from parent
            elif parent.state[0] + 1 == node.state[0]:
                stack.append("DOWN")
            # Up from parent
            elif parent.state[0] - 1 == node.state[0]:
                stack.append("UP")

            node = parent

        # Flip commands to go from root to passed node
        stack.reverse()

        return stack

    def search(self, start: tuple, target: tuple, gameState: State):
        # Set up initial dictionary and prio queu
        self.reached = {}
        self.frontier = []

        # Create Initial A* Node
        cur_node = TNode(0, 0, self.heuristic(start, target), start, None)

        # Set up search
        self.reached[cur_node.state] = cur_node
        heappush(self.frontier, cur_node)

        while self.frontier:
            # Get next node
            cur_node = heappop(self.frontier)
            
            # Check terminal state
            if self.is_goal(cur_node.state, target):
               return cur_node

            # Get successors and add to heap
            for state in self.successors(cur_node.state[0], cur_node.state[1]):
                ch = self.gameboard.board[state[0]][state[1]].ch

                # Only allow C as a path if the game is trying to reach the controller
                if ch == "C" and gameState != State.CONTROL:
                    continue
                
                # Ignore any walls or unknown tiles when planning a path
                if ch != '#' and ch != '?':
                    # Calculate next G, H, and F value
                    g = 1 + self.reached[cur_node.state].g
                    h = self.heuristic(state, target)
                    f = g + h

                    # Make successor node
                    node = TNode(f, g, h, state, cur_node)

                    # Update dictionary and heap
                    if node.state not in self.reached or node.f < self.reached[node.state].f:
                        self.reached[node.state] = node
                        heappush(self.frontier, node)


class BFS(Search):
    def __init__(self, board: Board, v=False):
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
                if (n.ch == 'T' or n.ch == '.') and n not in self.reached:
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


class Game:
    def __init__(self, board: Board, verbose=False):
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

def main():

    # Auto-generated code below aims at helping you parse
    # the standard input according to the problem statement.
    # r: number of rows.
    # c: number of columns.
    # a: number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
    r, c, a = [int(i) for i in input().split()]

    # Set up board, game
    board = Board(c, r)
    game = Game(board, False)
    game.printError("Rows: " + str(r) + ", Columns: " + str(c))
    # Set up search classes
    astar = AStar(board, a, False)
    bfs = BFS(board, False)
    
    # game loop
    while True:
        # kr: row where Kirk is located.
        # kc: column where Kirk is located.
        kr, kc = [int(i) for i in input().split()]

        game.printError("Kirt Row: " + str(kr) + ", Kirt Col: " + str(kc))

        for x in range(r):
            # C of the characters in '#.TC?' (i.e. one line of the ASCII maze).
            row = input()
            game.printError(row)
            board.updateRow(x, row)

        # If I already have moves queued
        if game.moves:
            # pop next command and execute it
            print(game.nextMove())
        else:
            tup = (kr, kc)
            start = (board.start.x, board.start.y)
            if board.control:
                cntrl = (board.control.x, board.control.y)

            # Print initial state of turn
            game.printError(game.state)
            if game.state == State.EXPLORE:
                game.printError("IN EXPLORE BLOCK")
                
                # Switch state only if all squares are discovered
                if bfs.checkFull():
                    game.printError("Changing Game State to CONTROL")
                    game.updateState(State.CONTROL)
                # If I can make it to the control panel and back in time 
                elif board.control and bfs.search(start, 'C') and len(astar.getPath(astar.search(cntrl, start, game.state))) <= astar.alarm:
                    game.printError("Can make it in time")
                    game.updateState(State.CONTROL)
                # Else find closest "?" tile
                else:
                    game.printError("Getting next ?")
                    
                    # Get cords to the closest unknown tile
                    cords = bfs.search(tup, "?")
                    game.printError("Row : " + str(cords[0]) + ", Col: " + str(cords[1]) + ", Char: " + board.board[cords[0]][cords[1]].ch)
                    
                    # Get path to those cords 
                    node = astar.search(tup, cords, game.state)
                    stack = astar.getPath(node)
                    game.printError(stack)
                    
                    # Add moves to the queue 
                    game.addMoves(stack)

            # Print state in case of change
            game.printError(game.state)
            if game.state == State.CONTROL:
                game.printError("IN CONTROL BLOCK")

                # Check if I am at the console
                if kr == board.control.x and kc == board.control.y:
                    game.printError("Changing Game State to ESCAPE")
                    game.updateState(State.ESCAPE)
                # Find path to the console
                else:
                    game.printError("Getting path to control panel")
                    
                    # Find path from current position to the console
                    node = astar.search(tup, (board.control.x, board.control.y), game.state)
                    stack = astar.getPath(node)
                    game.printError(stack)

                    # Add moves to the queue 
                    game.addMoves(stack)

            # Print state in case of change      
            game.printError(game.state)
            if game.state == State.ESCAPE:
                game.printError("IN ESCAPE BLOCK")

                # Find path from the console to the starting position
                node = astar.search(tup, (board.start.x, board.start.y), game.state)
                stack = astar.getPath(node)
                game.printError(stack)

                # Add moves to the queue 
                game.addMoves(stack)

            # pop next command and execute it
            print(game.nextMove())
            
if __name__ == '__main__':
    main()
