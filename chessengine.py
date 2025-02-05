class GameState:
    def __init__(self):
        """
        The board is an 8x8 2D list. Each element of the list has 2 characters:
        - The first character represents the color of the piece: 'b' (black) or 'w' (white).
        - The second character represents the type of the piece: 'K', 'Q', 'R', 'B', 'N', or 'P'.
        - '--' represents an empty space with no piece.
        """
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enpassantPossible = ()  # coordinates for the square where en passant capture is possible
        self.currentCastlingRight = castleRights(True, True, True, True)
        self.castlingRightsLog = [castleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]  # to keep track of the castling rights
        """
        you don't refrence directly to the currentCastlingRight object in the castlingRightsLog list because if you change the currentCastlingRight object
        then the object in the list will also change. Hence you create a new object with the same values as the currentCastlingRight object and append it to the list
        in order to make a snapshot of the castling rights at that point in time"""

    ## to make move on the board
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        # pawn promotion
        if move.pawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
        # enpassant move 
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--" # capturing the pawn
            """
            startRow as the captured pawn in the same row as the pawn that moved 
            and endcol as the column of the pawn that moved"""
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: # pawn moved 2 squares only on the first move
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
            """
            enpassant possible in the square between the initial and final square of the pawn that moved"""
        else:
            self.enpassantPossible = ()

        # castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: # king side castle move
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] #end row and end col is the king landing square
                self.board[move.endRow][move.endCol+1] = "--" # remove the rook from the original square
            else: # queen side castle move
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] 
                self.board[move.endRow][move.endCol-2] = "--"
            
        # update castling rights
        self.updateCastleRights(move)
        self.castlingRightsLog.append(castleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))


    def undomove(self):
        if len(self.moveLog)!= 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bk':
                self.blackKingLocation = (move.startRow, move.startCol)
            # undo enpassant move
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--" # leave landing square empty
                self.board[move.startRow][move.endCol] = move.pieceCaptured # put the captured piece back
                self.enpassantPossible = (move.endRow, move.endCol)
            # undo 2 square pawn advance
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = () # enpassant is only possible for 1 move
            
            # undo castling rights
            self.castlingRightsLog.pop() 
            newRights = self.castlingRightsLog[-1] # set the current castling rights to the last element iin the list 
            self.currentCastlingRight = castleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            # undo castling move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = "--"
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = "--"

            self.checkmate = False
            self.stalemate = False


    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: # left rook
                    self.currentCastlingRight.wqs = False
                else :
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: # left rook
                    self.currentCastlingRight.bqs = False
                else :
                    self.currentCastlingRight.bks = False

    def getvalidmoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempcastlingRights = castleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                           self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        
        moves = self.getAllPossibleMoves()

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        for i in range(len(moves)-1,-1,-1): # when removing from a list go backwards through that list 
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove 
            """
            you have made a move and hence the turn has changed to the oppenent so you want to switch the turns again to get the valid 
            moves for the player who made the move
            """
            if self.inCheck(): # if the player king is in check then the move is invalid
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove # switch back to the actual player turn
            self.undomove() # hence undo the move to get the actual board state thus this move is not made and not valid
        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempcastlingRights


        return moves

    
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1]) 

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
            
        return False  

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                piece = self.board[r][c][1]
                if (self.whiteToMove and turn == 'w') or (not self.whiteToMove and turn == 'b'):
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
                    elif piece == 'N':
                        self.getKnightMoves(r, c, moves)
                    elif piece == 'B':
                        self.getBishopMoves(r, c, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r, c, moves)
                    elif piece == 'K':
                        self.getKingMoves(r, c, moves)
        return moves
    
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            # Move one square forward
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                # Move two squares forward from starting position
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            # Capturing moves
            if c-1 >= 0:  # Capture to the left
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible: # en passant capture
                    moves.append(Move((r,c),(r-1,c-1),self.board,isEnpassantMove=True))
            if c+1 <= 7:  # Capture to the right
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible: # en passant capture
                    moves.append(Move((r,c),(r-1,c+1),self.board,isEnpassantMove=True))
        else:
            # Move one square forward
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                # Move two squares forward from starting position
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            # Capturing moves
            if c-1 >= 0:  # Capture to the left
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible: # en passant capture
                    moves.append(Move((r,c),(r+1,c-1),self.board,isEnpassantMove=True))

            if c+1 <= 7:  # Capture to the right
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible: # en passant capture
                    moves.append(Move((r,c),(r+1,c+1),self.board,isEnpassantMove=True))

        

    def getRookMoves(self, r, c, moves):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):  # Rook can move max 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break
        
        

    def getKnightMoves(self, r, c, moves):
        knightMoves = [(-2, -1), (-1, -2), (1, -2), (2, -1),(2, 1), (1, 2), (-1, 2), (-2, 1)]
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" or endPiece[0] != allyColor:  # empty or enemy piece
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getBishopMoves(self, r, c, moves):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # 4 diagonal directions
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):  # Bishop can move max 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break
    
    def getKingMoves(self, r, c, moves):
        kingMoves = [
            (-1, -1), (-1, 0), (-1, 1),  # up-left, up, up-right
            (0, -1),         (0, 1),     # left,       right
            (1, -1), (1, 0), (1, 1)      # down-left, down, down-right
        ]
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" or endPiece[0] != allyColor:  # empty or enemy piece
                    moves.append(Move((r, c), (endRow, endCol), self.board))
        


    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return 
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMoves(r, c, moves)

        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(r, c, moves)


    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r,c),(r,c+2),self.board,isCastleMove = True))
            
    
    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r,c),(r,c-2),self.board,isCastleMove = True))


class castleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

## to keep track of the moves and the pieces that are moved and captured and the board
class Move:
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # pawn promotion
        self.pawnPromotion = False
        if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7):
            self.pawnPromotion = True
        # enpassant move
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'

        # castle move
        self.isCastleMove = isCastleMove

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow *10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self): 
       return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):  # helper function to get rank file [0,7] -> "a8"
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
