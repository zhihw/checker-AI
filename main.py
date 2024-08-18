from board import Board
from MCTS import MCTS
import copy
def print_board(state):
    for row in state:
        print(" ".join(str(x) for x in row))
    print()

def main():
    state = Board.initialize_board()
    board = Board(state)
    finished = False
    winner = 0
    while True:
        print_board(board.state)
        while True:
            try:
                user_input = input("The current position of your chess piece, the position you need to move to:x1,y1,x2,y2 ")
                x1, y1, x2, y2 = map(int, user_input.split())
                piece = board.Piece((x1, y1), board.state[x1][y1])
                if (piece.value == 1 or piece.value == 10) and board.is_legal(piece, (x2, y2)):
                    board.make_move(piece, (x2, y2))
                    break
                else:
                    print("invalid move")
            except (ValueError, IndexError):
                print("the input is not valid")
            finished, winner = board.is_final()
        print_board(board.state)
        if finished==True:
            if winner == 1:
                print("you win")
            elif winner == -1:
                print("agent win")
            else:
                print("draw")
            break
        x=copy.deepcopy(board)
        mcts_agent=MCTS(x,-1,10)
        best_board = mcts_agent.search()
        board.state = best_board.state
        if finished:
            if winner == 1:
                print("you win")
            elif winner == -1:
                print("agent win")
            else:
                print("draw")
            break


if __name__ == "__main__":
    main()
    