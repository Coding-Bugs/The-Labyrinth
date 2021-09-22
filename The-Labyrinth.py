from classes.state import State
from classes.game import Game
from classes.board import Board
from classes.astar import AStar
from classes.bsf import BFS

def main():
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
    