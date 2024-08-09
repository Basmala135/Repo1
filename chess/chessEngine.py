# this class is responsible for storing all the current info about the game also determining the valid moves 

class gameState():
    def __init__(self):
        self.board = [['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
                      ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                      ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']]
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove  # switching the players

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'r':
                        self.getRookMoves(r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn moves
            if self.board[r-1][c] == "--":  # 1 square move
                moves.append(move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":  # 2 squares move
                    moves.append(move((r, c), (r-2, c), self.board))
            if c-1 >= 0:  # capture to the left
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:  # capture to the right
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(move((r, c), (r-1, c+1), self.board))
        else:  # black pawn moves
            if self.board[r+1][c] == "--":  # 1 square move
                moves.append(move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":  # 2 squares move
                    moves.append(move((r, c), (r+2, c), self.board))
            if c-1 >= 0:  # capture to the left
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7:  # capture to the right
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(move((r, c), (r+1, c+1), self.board))

    def getRookMoves(self, r, c, moves):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space valid
                        moves.append(move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break

class move():
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCap = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, move):
            return self.moveID == other.moveID
        return False
