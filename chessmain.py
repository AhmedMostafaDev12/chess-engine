import chessengine
import pygame as p 
import AI

p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock  = p.time.Clock()
    gs = chessengine.GameState()
    validMoves = gs.getvalidmoves()
    movemade = False
    animate = False
    loadImages()

    running = True
    sqSelected = ()  ## No square is selected initially
    playerClicks = []  ## Keep track of player clicks [(6,4), (4,4)]
    gameover = False
    playerone = True #if human is playnig white, then this will be True, if AI is playing , then this will be False
    playertwo = False #if human is playnig black, then this will be True, if AI is playing , then this will be False
    while running:
        humanTurn = (gs.whiteToMove and playerone) or (not gs.whiteToMove and playertwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameover and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE  

                    if sqSelected == (row, col):  # Clicked the same square twice
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # Append for both clicks
                    
                    if len(playerClicks) == 2:  # After the second click
                        move = chessengine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                movemade = True
                                animate = True

                                sqSelected = ()  # Reset user clicks
                                playerClicks = []
                        if not movemade:
                            playerClicks = [sqSelected] # If the move was invalid, keep the first click

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Undo move when "Z" is pressed
                    gs.undomove()
                    movemade = True
                    animate = False
                if e.key == p.K_r:  # Reset the board when "R" is pressed
                    gs = chessengine.GameState()
                    validMoves = gs.getvalidmoves()
                    sqSelected = ()
                    playerClicks = []
                    animate = False
                    movemade = False
                    gameover = False
 
        #AI move finder logic

        if not gameover and not humanTurn:
            AImove = AI.findBestMove(validMoves, gs)
            if AImove is None:
                AImove = AI.findRandomMove(validMoves)
            gs.makeMove(AImove)
            movemade = True
            animate = True

        
        if movemade:  # If a move was made, update the board
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getvalidmoves()
            movemade = False
            animate = False


        drawgamestate(screen, gs, validMoves , sqSelected)  # Draw board and pieces

        if gs.checkmate:
            gameover = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
           
        
        elif gs.stalemate:
            gameover = True
            drawText(screen, 'Stalemate')
           

        clock.tick(MAX_FPS)
        p.display.flip()

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # Transparency value
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))

def drawgamestate(screen, gs, validMoves, sqSelected):
    drawboard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawpieces(screen, gs.board)

def drawboard(screen):
    global colors
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawpieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # If there's a piece in this square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

import pygame as p

def animateMove(move, screen, board, clock):
    global colors
    # Calculate the row and column displacement (how many squares the piece moves)
    dR = move.endRow - move.startRow  
    dC = move.endCol - move.startCol  

    # Number of frames to move one square (controls animation smoothness)
    framesPerSquare = 10  
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare  # Total frames for the animation

    # Animate movement frame by frame
    for frame in range(frameCount + 1):
        # Calculate the interpolated (in-between) position of the piece for this frame
        r = move.startRow + dR * frame / frameCount
        c = move.startCol + dC * frame / frameCount

        # Redraw the board and all pieces before updating the moving piece
        drawboard(screen)
        drawpieces(screen, board)

        # Determine the color of the destination square (alternating light/dark pattern)
        color = colors[(move.endRow + move.endCol) % 2]

        # Define the rectangle representing the final destination square
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)

        # Redraw the destination square with its original color
        p.draw.rect(screen, color, endSquare)

        # If a piece was captured, redraw it at its final position before moving the new piece
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)

        # Draw the moving piece at its current interpolated position
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

        # Update the display to reflect the new frame
        p.display.flip()

        # Control the animation speed (frames per second)
        clock.tick(60)  # Runs at 60 FPS to ensure smooth animation

def drawText(screen, text):
    font = p.font.SysFont('Helvitca', 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2, HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))


if __name__ == "__main__":
    main()
