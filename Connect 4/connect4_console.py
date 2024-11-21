import numpy as np
import pygame

'''
Structure:
    1. the game board is created 
    2. player 1 will make a selection for a column between 0 and 6
    3. the location they choose will be checked to see whether the number of 
        pieces that have been already placed in that slot, and if there is a 
        vacancy, then the piece will be dropped
'''
    

# Parameters:
    
WIDTH = 1000
HEIGHT = 800


class Game:
    def __init__(self):
        
        # create elements of the game
        self.board = np.zeros((6,7))
        self.turn = 0
        self.p1_pieces = []
        self.p2_pieces = []
    
    
    def drop_piece(self,coord):
        self.board[coord[0], coord[1]] = self.turn + 1
        if self.turn == 0:
            self.p1_pieces.append(coord)
        elif self.turn == 1:
            self.p2_pieces.append(coord)
        else:
            print("error: it is neither player 1 or player 2's turn")
    
    
    def is_valid(self,col):
        # returns the position of the next vacant position or returns -1 if 
        # there are no positions left
        if col != '': 
            col = int(col)
            if col >= 0 and col <= 6:
                return True
        return False
    
    def find_next_pos(self, col):
        col_to_check = self.board[:, col]
        for i, e in reversed(list(enumerate(col_to_check))):
            if e == 0:
                # print(i)
                # print(type(i))
                return int(i)
        return -1
        
    
    def is_row(self):
        
        # print('is_row processing')
        if self.turn == 0:
            pieces = self.p1_pieces
            
        elif self.turn == 1:
            pieces = self.p2_pieces
        
        for piece in pieces:
            # print(piece)
            row = piece[0]
            col = piece[1]
            if col >= 0 and col <= 3:
                row_to_check = self.board[row, col:col+4]
                # print(row_to_check)
                if len(np.unique(row_to_check)) == 1 and row_to_check[0] == self.turn + 1:
                    return True
    
    
    def is_col(self):
        
        # print('is_col processing')
        if self.turn == 0:
            pieces = self.p1_pieces
            
        elif self.turn == 1:
            pieces = self.p2_pieces
        
        for piece in pieces:
            # print(piece)
            row = piece[0]
            col = piece[1]
            if row >= 0 and row <= 2:
                col_to_check = self.board[row: row+4, col]
                # print(col_to_check)
                if len(np.unique(col_to_check)) == 1 and col_to_check[0] == self.turn + 1:
                    return True
                
                
    def is_diag_NE(self):
        
        # print('is_diag_NE processing')
        if self.turn == 0:
            pieces = self.p1_pieces
            
        elif self.turn == 1:
            pieces = self.p2_pieces
        
        for piece in pieces:
            # print(piece)
            row = piece[0]
            col = piece[1]
            if col >= 0 and col <= 3 and row >= 3 and row <= 5:
                diag_to_check = []
                for i in range(4):
                    diag_to_check.append(self.board[row,col])
                    col = col + 1
                    row = row - 1
                # print(diag_to_check)

                if len(np.unique(diag_to_check)) == 1 and diag_to_check[0] == self.turn + 1:
                    return True

    def is_diag_NW(self):
        
        # print('is_diag_NW processing')
        if self.turn == 0:
            pieces = self.p1_pieces
            
        elif self.turn == 1:
            pieces = self.p2_pieces
        
        for piece in pieces:
            # print(piece)
            row = piece[0]
            col = piece[1]
            if col >= 3 and col <= 6 and row >= 3 and row <= 5:
                diag_to_check = []
                for i in range(4):
                    diag_to_check.append(self.board[row,col])
                    col = col - 1
                    row = row - 1
                # print(diag_to_check)

                if len(np.unique(diag_to_check)) == 1 and diag_to_check[0] == self.turn + 1:
                    return True

    def run(self):

        game_over = False        
        
        while not game_over:
            # Ask for Player 1 input
            if self.turn == 0:
                col = input("Player 1 Make your selection (0-6): ")
                        
            # Ask for Player 2 input 
            if self.turn == 1:
                col = input("Player 2 Make your selection (0-6): ")
                
            if self.is_valid(col):
                col = int(col)
                row = self.find_next_pos(col)
                if row != -1:
                    self.drop_piece([row,col])
                    print(self.board)
                        
                    if self.is_row() or self.is_col() or self.is_diag_NE() or self.is_diag_NW():
                        print(f'\nGAME OVER! Player {self.turn+1} wins')
                        game_over = True
                    
                    
                    print()
                    
                    self.turn = (self.turn + 1) % 2
            else:
                print("invalid move! please try again")
            

            
if __name__ == '__main__':
    game = Game()
    game.run()