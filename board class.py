class Node:
    def __init__(self,state,children,value,is_max=True):
        self.state=state
        self.children=children
        self.value=0
        self.is_max=is_max




class Board:
    class Piece:
        def __init__(self, position, value):
            self.position = position  # position like [i,j]
            self.value = value #1=player1 -1=player2 10=player1king -10=player2king 

    def __init__(self,state):
        self.state=state

    #Generate a chessboard. The initial state is that all positions without chess pieces are 0, 
    #positions with chess pieces are 1 or -1, representing the two players respectively.
    def initialize_borad():
        board = [[0] * 8 for _ in range(8)]
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 != 0:
                    if i < 3:
                        board[i][j] = -1  
                    elif i > 8 - 4:
                        board[i][j] = 1 
        return board
    
    def is_legal(self,piece,position):
        x1,x2=piece.position
        y1,y2=position
        
        if not (0 <= x2 < 8 and 0 <= y2 < 8):
            return False
                
        if self.state[x2][y2] != 0:
            return False
        
        if piece.value ==1:
            if x1-y1==1 and abs(x1-y1)==1:
                return True
        if piece.value ==-1:
            if y1-x1==1 and abs(x1-y1)==1:
                return True
            
        if piece.value in [10,-10]:
            if abs(x1-y1)==abs(x2-y2):
                return True
            


            



    def legal_moves(state):
        actions=[]
        
