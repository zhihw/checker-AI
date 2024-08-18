from itertools import product
from random import choice

class Board:
    class Piece:
        def __init__(self, position, value):
            self.position = position  # position like [i,j]
            self.value = value #1=player1 -1=player2 10=player1king -10=player2king 

    def __init__(self,state):
        self.state=state

    #Generate a chessboard. The initial state is that all positions without chess pieces are 0, 
    #positions with chess pieces are 1 or -1, representing the two players respectively.
    def initialize_board():
        board = [[0] * 8 for _ in range(8)]
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 != 0:
                    if i < 3:
                        board[i][j] = -1  
                    elif i > 8 - 4:
                        board[i][j] = 1 
        return board
    

    def is_legal(self, piece, position):
        x1, x2 = piece.position
        y1, y2 = position
    
        if not (0 <= y1 < 8 and 0 <= y2 < 8):
            return False
    
        if self.state[y1][y2] != 0:
            return False
    
        if piece.value == 1:  
            if x1 - y1 == 1 and abs(x2 - y2) == 1:
             return True
            if x1 - y1 == 2 and abs(x2 - y2) == 2:
                if 0 <= x1 - 1 < 8 and 0 <= (x2 + (y2 - x2) // 2) < 8:
                    if self.state[x1 - 1][x2 + (y2 - x2) // 2] < 0:
                        return True
    
        if piece.value == -1:  
            if y1 - x1 == 1 and abs(x2 - y2) == 1:
                return True
            if y1 - x1 == 2 and abs(x2 - y2) == 2:
                if 0 <= x1 + 1 < 8 and 0 <= (x2 + (y2 - x2) // 2) < 8:
                    if self.state[x1 + 1][x2 + (y2 - x2) // 2] > 0:
                        return True
    
        if piece.value in [10, -10]:  
            if abs(x1 - y1) == 1 and abs(x2 - y2) == 1:
                return True
            if abs(x1 - y1) == 2 and abs(x2 - y2) == 2:
                if 0 <= (x1 + (y1 - x1) // 2) < 8 and 0 <= (x2 + (y2 - x2) // 2) < 8:
                    if self.state[x1 + (y1 - x1) // 2][x2 + (y2 - x2) // 2] * piece.value < 0:
                        return True

        return False

    def legal_moves(self):
        actions=[]
        jump_actions = []
        for i,j in product(range(8),range(8)):
            if self.state[i][j] != 0:
                piece = self.Piece((i,j),self.state[i][j])
                for (i1,j1) in product(range(i-2,i+3),range(j-2,j+3)):
                    if self.is_legal(piece,(i1,j1)):
                        actions += [(piece,(i1,j1))]
        return actions

    def make_move(self,piece,position): #assume move is valid
        x1,x2 = piece.position
        y1,y2 = position

        self.state[y1][y2] = self.state[x1][x2]
        self.state[x1][x2] = 0

        if abs(x1-y1) == 2:
            self.state[x1+(y1-x1)//2][x2+(y2-x2)//2] = 0
        
        if y1 == 0 and piece.value == 1:
            self.state[y1][y2] = 10
        elif y1 == 7 and piece.value == -1:
            self.state[y1][y2] = -10


    def is_final(self):
        legal_moves = self.legal_moves()

        if not legal_moves:
            player1_pieces = sum(1 for row in self.state for piece in row if piece > 0)
            player2_pieces = sum(1 for row in self.state for piece in row if piece < 0)
        
            if player1_pieces > 0 and player2_pieces == 0:
                return True, 1  # Player 1 wins
            elif player2_pieces > 0 and player1_pieces == 0:
                return True, -1  # Player 2 wins
            else:
                return True, 0  # Draw 

        return False, 0  # Game is not over
                
    def random_move(self,team):
        legal_moves = self.legal_moves()
        if legal_moves:
                filtered_moves = [move for move in legal_moves if move[0].value in [team, 10*team]]
                if filtered_moves:
                     return choice(filtered_moves)
                else: 
                    return None
        else:   
            return None

    def random_game(self,team):
        finished,winning_team = self.is_final()
        while not finished:
           
            move = self.random_move(team)
            if move is None:
                finished = True
                winning_team = -team  
                break
            piece = move[0]
            position = move[1]
            self.make_move(piece,position)
            finished,winning_team = self.is_final()
            team = -team
        return winning_team
