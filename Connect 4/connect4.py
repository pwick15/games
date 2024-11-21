import numpy as np
import pygame
from pygame.locals import *
import time
import os

# PARAMETERS
CIRCLE_OFFSET = 15
CIRCLESIZE = 70
SQUARESIZE = 640/7
ROWS = 6
COLS = 7
WIDTH = SQUARESIZE * COLS
HEIGHT = SQUARESIZE * (ROWS+1)
SIZE = (WIDTH, HEIGHT)
P1_PATH = 'red_circle.png'
P2_PATH = 'yellow_circle.png'

class Board:
    def __init__(self, surface) -> None:
        self.surface = surface
        self.board = pygame.image.load('Connect4Board.png')
        
    def draw(self):
        self.surface.blit(self.board, (0,HEIGHT - 480))


class FloatPiece:
    def __init__(self, surface) -> None:
        self.pos_x = CIRCLE_OFFSET
        self.pos_y = HEIGHT - 480 - CIRCLESIZE
        self.surface = surface
        self.piece = pygame.image.load(P1_PATH)
        self.piece = pygame.transform.scale(self.piece, (CIRCLESIZE,CIRCLESIZE))


    def draw(self,turn):
        if turn == 0:
            self.piece = pygame.image.load(P1_PATH)
            self.piece = pygame.transform.scale(self.piece, (CIRCLESIZE,CIRCLESIZE))
        if turn == 1:
            self.piece = pygame.image.load(P2_PATH)
            self.piece = pygame.transform.scale(self.piece, (CIRCLESIZE,CIRCLESIZE))
        self.surface.blit(self.piece, (self.pos_x, self.pos_y))

class P1Piece:
    def __init__(self, surface) -> None:
        self.surface = surface
        self.p1_piece = pygame.image.load(P1_PATH)
        self.p1_piece = pygame.transform.scale(self.p1_piece, (CIRCLESIZE,CIRCLESIZE))
    
    def draw_p1(self, pos_x, pos_y):
        self.surface.blit(self.p1_piece, (pos_x, pos_y))

class P2Piece:
    def __init__(self, surface) -> None:
        self.surface = surface
        self.p2_piece = pygame.image.load(P2_PATH)
        self.p2_piece = pygame.transform.scale(self.p2_piece, (CIRCLESIZE,CIRCLESIZE))
    
    def draw_p2(self, pos_x, pos_y):
        self.surface.blit(self.p2_piece, (pos_x, pos_y))

class Game:
    def __init__(self) -> None:

        #set position of window
        x = 60000
        y = 400
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)   

        # initialise pygame
        pygame.init()

        # create background
        self.surface = pygame.display.set_mode(SIZE)
        
        # create lists to store locations of pieces that have been placed
        self.p1_list = []
        self.p2_list = []

        # add board
        self.board = Board(self.surface)
        self.board.draw()

        # initialise back-end of game
        self.turn = 0
        self.backend_board = np.zeros((6,7))
        self.p1_pieces = []
        self.p2_pieces = [] 

        # add piece
        self.piece = FloatPiece(self.surface)
        self.piece.draw(self.turn)        

        # display
        pygame.display.flip()

    def find_next_pos(self, col):
        col_to_check = self.backend_board[:, col]
        for i, e in reversed(list(enumerate(col_to_check))):
            if e == 0:
                return int(i)
        return -1

    def drop_piece(self,coord):
        row = coord[0]
        col = coord[1]
        self.backend_board[row, col] = self.turn + 1
        # print(self.backend_board)

        new_pos_x = 15 + col * 90
        new_pos_y = 565 - (5-row) * 80
        
        if self.turn == 0:
            self.p1_pieces.append(coord)
            self.p1_list.append([new_pos_x, new_pos_y])
            # print(self.p1_list)
        elif self.turn == 1:
            self.p2_pieces.append(coord)
            self.p2_list.append([new_pos_x, new_pos_y])
            # print(self.p2_list)
        else:
            print("error: it is neither player 1 or player 2's turn")

    def is_row(self):
        
        if self.turn == 0:
            pieces = self.p1_pieces
            
        elif self.turn == 1:
            pieces = self.p2_pieces
        
        for piece in pieces:
            row = piece[0]
            col = piece[1]
            if col >= 0 and col <= 3:
                row_to_check = self.backend_board[row, col:col+4]
                if len(np.unique(row_to_check)) == 1 and row_to_check[0] == self.turn + 1:
                    return True

    def is_col(self):
        
        if self.turn == 0:
            pieces = self.p1_pieces
            
        elif self.turn == 1:
            pieces = self.p2_pieces
        
        for piece in pieces:
            row = piece[0]
            col = piece[1]
            if row >= 0 and row <= 2:
                col_to_check = self.backend_board[row: row+4, col]
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
                    diag_to_check.append(self.backend_board[row,col])
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
                    diag_to_check.append(self.backend_board[row,col])
                    col = col - 1
                    row = row - 1
                # print(diag_to_check)

                if len(np.unique(diag_to_check)) == 1 and diag_to_check[0] == self.turn + 1:
                    return True


    def new_frame(self):
        self.surface.fill((111,111,111))
        self.board.draw()
        self.piece.draw(self.turn)

        for piece_loc in self.p1_list:
            p1_piece = P1Piece(self.surface)
            p1_piece.draw_p1(piece_loc[0], piece_loc[1])
        for piece_loc in self.p2_list:
            p2_piece = P2Piece(self.surface)
            p2_piece.draw_p2(piece_loc[0], piece_loc[1])
        pygame.display.flip()

    def run(self):
        running = True

        while running:

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    pass
                    
                # moving the piece around
                if event.type == MOUSEMOTION:
                    self.piece.pos_x = pygame.mouse.get_pos()[0] - CIRCLESIZE/2
                    # self.piece.pos_y = pygame.mouse.get_pos()[1] - CIRCLESIZE/2

                # attempting to select a column to place a piece
                if event.type == MOUSEBUTTONDOWN:
                    # print(pygame.mouse.get_pos())
                    col = int(pygame.mouse.get_pos()[0] // SQUARESIZE)
                    # print(f'chosen column: {col}')
                    row = self.find_next_pos(col)
                    # print(f'chosen row: {row}')
                    if row != -1:
                        self.drop_piece([row,col])
                        

                        if self.is_row() or self.is_col() or self.is_diag_NE() or self.is_diag_NW():
                            print(f'\nGAME OVER! Player {self.turn+1} wins')
                            # running = False
                        
                        self.turn = (self.turn + 1) % 2
                if event.type == QUIT:
                    running = False

            self.new_frame()
            time.sleep(0.01)

if __name__ == '__main__':
    game = Game()
    game.run()