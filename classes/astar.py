from collections import namedtuple
from heapq import heappush, heappop

from search import Search
from state import State

TNode = namedtuple('TNode', ['f', 'g', 'h', 'state', 'parent'])

class AStar (Search):

    def __init__(self, board, alarm: int, v=False):
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