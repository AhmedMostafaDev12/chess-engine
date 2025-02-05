import random 
import chessengine 

pieceValues = {'p': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
checkMate = 1000
staleMate = 0
DEPTH = 2

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

# first one itereate through all the valid moves and find the best move
def explain(validMoves,gs):
    turnMultiplier = 1 if gs.whiteToMove else -1  
    '''
    we are starting in the prespictive of black player 
    and since we trying to maximize the score,we starting with the worst possible score
    from the black player prespective
    which is the positive checkmate score '''
    opponentMinMaxScore = checkMate 
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponent = gs.getvalidmoves()
        #opponent max score is the worst possible score from the white player prespective
        # which is the negative checkmate score
        if gs.checkmate:
            opponentsMaxScore = -checkMate
        elif gs.stalemate:
            opponentsMaxScore = staleMate
        else:
            opponentsMaxScore = -checkMate
            for opponentsMove in opponent:
                gs.makeMove(opponentsMove)
                #in all cases your score is the negative of the opponents score
                if gs.checkmate:
                    score =  checkMate
                elif gs.stalemate:
                    score = staleMate
                else:
                    score = -turnMultiplier * scoreMaterial(gs,gs.board)
                if score > opponentsMaxScore:
                    opponentsMaxScore = score
                    
                gs.undomove()
        if opponentsMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentsMaxScore
            bestPlayerMove = playerMove
        gs.undomove()
    
    return bestPlayerMove

def findBestMove(validMoves,gs):
    global nextMove
    nextMove = None 
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    findMoveNegaMaxAlphaBeta(gs, validMoves,DEPTH,-checkMate, checkMate, 1 if gs.whiteToMove else -1 )

    return nextMove

# doing minmax algorithm recursively
def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    if whiteToMove:
        maxscore = -checkMate 
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getvalidmoves()
            # recurisve call 
            score = findMoveMinMax(gs, nextMoves, depth-1, False)
            if score > maxscore :
                maxscore = score 
                if depth == DEPTH:
                    nextMove = move
            gs.undomove()
        return maxscore
    
    else:
        minscore = checkMate 
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getvalidmoves()
            # recursive call 
            score = findMoveMinMax(gs, nextMoves, depth-1, True)
            if score < minscore :
                minscore = score 
                if depth == DEPTH:
                    nextMove = move
            
            gs.undomove()
        return minscore


#minmax algorithm with alpha beta pruning
def findMoveNegaMaxAlphaBeta(gs, validMoves , depth ,alpha,beta, multiplier):
    #alpha is the max current score so we start with the lowest possible score
    #beta is the min current score so we start with the higher possible score
    global nextMove
    if depth == 0:
        return multiplier * scoreBoard(gs)
    maxscore = -checkMate
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getvalidmoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves ,depth -1 , -beta, -alpha, -multiplier)

        if score > maxscore :
            maxscore = score 
            if depth == DEPTH:
                nextMove = move 
        gs.undomove()
        if maxscore > alpha:
            alpha = maxscore
        if alpha >= beta:
            break
        
        
    return maxscore 




def scoreBoard(gs):

    if gs.checkmate:
        # if the game is over and the current player is in checkmate
        # and the white to move then white in the checkmate
        if gs.whiteToMove:
            return -checkMate
        else:
            return checkMate
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceValues[square[1]]
            elif square[0] == 'b':
                score -= pieceValues[square[1]]

    return score

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceValues[square[1]]
            elif square[0] == 'b':
                score -= pieceValues[square[1]]

    return score
    