import numpy as np
import pygame
import sys

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROWS = 6
COLS = 7

def create_board():
    board = np.zeros((ROWS, COLS))
    return board

def draw_board(board):
    
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQSIZE, r * SQSIZE + SQSIZE, SQSIZE, SQSIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQSIZE + SQSIZE / 2), int(r * SQSIZE + SQSIZE + SQSIZE / 2)), RADIUS)
        
    for c in range(COLS):
        for r in range(ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQSIZE + SQSIZE / 2), height - int(r * SQSIZE + SQSIZE / 2)), RADIUS)

            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQSIZE + SQSIZE / 2), height - int(r * SQSIZE + SQSIZE / 2)), RADIUS)
    pygame.display.update() 

def play(board, col, piece):
    global running

    def is_valid_location():
        return board[ROWS - 1][col] == 0
   
    def get_empty_row():
        for r in range(ROWS):
            if board[r][col] == 0:
                return r
    
    def drop_piece(row):
        board[row][col] = piece
        return board

    def winning_move():
        
        # Horizontal
        for c in range(COLS - 3):
            for r in range(ROWS):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True
       
        # Vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True 

        # Positive Diagonal
        for c in range(COLS-3):
            for r in range(ROWS-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                     return True 

     
        # Negative Diagonal
        for c in range(COLS-3):
            for r in range(3, ROWS):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True      
   
    if is_valid_location():
        row = get_empty_row()
        drop_piece(row)       
        
        if winning_move():
            ALERT.play()
            label = myfont.render("Player {} Wins!!! Congrats!!".format(piece), 1, RED)
            screen.blit(label, (40, 10))
            running = False
        

        if board.all():
            ALERT.play()
            label = myfont.render("Game TIE!!", 1, RED)
            screen.blit(label, (40, 10))
            running = False
        return running
    

board = create_board()
running = True
turn = 0

SQSIZE = 100

RADIUS = int(SQSIZE / 2 - 5)

pygame.init()
pygame.display.set_caption("Connect 4")

width = COLS * SQSIZE
height = (ROWS+1) * SQSIZE
size = (width, height)
screen = pygame.display.set_mode(size)
draw_board(board)

COIN_DROP = pygame.mixer.Sound("coin_drop.wav")
ALERT = pygame.mixer.Sound("alert.wav")
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQSIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQSIZE / 2)), RADIUS)

            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQSIZE / 2)), RADIUS)

        pygame.display.update()


        if event.type == pygame.MOUSEBUTTONDOWN:
            COIN_DROP.play()

            pygame.draw.rect(screen, BLACK, (0, 0, width, SQSIZE))
                        
            posx = event.pos[0]
            col = posx // SQSIZE
            # Ask for player 1 input
            if turn == 0:
                play(board, col, 1)
                           
            # Ask for player 2 input
            else:
                play(board, col, 2)
        
            turn += 1
            turn %= 2

            draw_board(board)
            
            if not running:
                pygame.time.wait(10000)
