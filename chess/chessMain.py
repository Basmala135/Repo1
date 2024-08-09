# this file is for handling user input and display current state obj 

import pygame as p
import chessEngine

p.init()

width = height = 520
dim = 8  # As chess board is 8x8
sq_size = height // dim  # It would give a nice ratio
max_fps = 15
images = {}

# Making function to load the images
def loadImages():
    pieces = ['bb','bk','bn','bp','bq','br','wb','wk','wn','wp','wq','wr']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load('pieces-png/' + piece + '.png'), (sq_size, sq_size))

def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.gameState()
    validMoves = gs.getValidMoves()
    movesMade = False
    loadImages()
    running = True
    squareSelected = None  # Keep track of the last square selected by the user
    playerClicks = []  # Keep track of the player clicks

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // sq_size
                row = location[1] // sq_size
                if squareSelected == (row, col):
                    squareSelected = None  # Resetting the squareSelected
                    playerClicks = []
                else:
                    squareSelected = (row, col)
                    playerClicks.append(squareSelected)
                if len(playerClicks) == 2:
                    move = chessEngine.move(playerClicks[0], playerClicks[1], gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        movesMade = True
                    squareSelected = None  
                    playerClicks = []
        if movesMade:
            validMoves = gs.getValidMoves()
            movesMade = False

        drawGameState(screen, gs)
        clock.tick(max_fps)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen)  # Draw squares on the board
    drawPieces(screen, gs.board)  # Draw pieces on the screen

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for i in range(dim):
        for j in range(dim):
            color = colors[((i + j) % 2)]
            p.draw.rect(screen, color, p.Rect(j * sq_size, i * sq_size, sq_size, sq_size))

def drawPieces(screen, board):
    for i in range(dim):
        for j in range(dim):
            piece = board[i][j]
            if piece != "--":
                screen.blit(images[piece], p.Rect(j * sq_size, i * sq_size, sq_size, sq_size))

if __name__ == "__main__":
    main()
